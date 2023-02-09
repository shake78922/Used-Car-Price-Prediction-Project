import collections
from django.shortcuts import render ,redirect, reverse
from django.views.generic import View

from carSearchSite.models import CarInfo,ImageModel,InferencedImage
from carSearchSite.forms import CarInfoForm, ImageUploadForm

from django.conf import settings
from django.contrib import messages
from django.utils.dateformat import DateFormat

import torch
import joblib 
import yolov5
from ast import literal_eval


from datetime import datetime
import os
import io
from PIL import Image as I

# Create your views here.
class CarSearchModel(View):
    def get(self,request):
        form = CarInfoForm()
        imageform = ImageUploadForm()
        
        context = {
            'form':form,
            'imageform':imageform
        }
        return render(request,"carSearchSite/model1.html",context)

    def post(self,request):     
           
        # 날짜데이터 (문자열 --> 날짜)
        cy = request.POST['carCalendar']
        cy_format = "%Y-%m-%d"
        cy_year = datetime.strptime(cy,cy_format)

        #연월만 추출
        year = int(DateFormat( cy_year).format("Y")) - 2000
        month = int(DateFormat( cy_year).format("m"))
        
        # 차를 사용한 개월 
        car_year = 300 - (year*12) - month
        
        #데이터베이스 저장
        carinfo = CarInfo()
        carinfo.carCalendar = request.POST['carCalendar'] # 차량 연식
        carinfo.carDistance = request.POST['carDistance'] # 차량 주행거리
        carinfo.carFuel = request.POST['carFuel'] # 차량 연료
       
        carinfo.carYear = year
        carinfo.carMonth = month
        carinfo.carModel = car_year
       
        # 딥러닝 모델
        img = request.FILES.get('image')
        img_instance = ImageModel(
            image=img
        )
        img_instance.save()

        uploaded_img_qs = ImageModel.objects.filter().last()
        img_bytes = uploaded_img_qs.image.read()
        img = I.open(io.BytesIO(img_bytes))
        uploaded_img_qs.image.close()
        
        path_hubconfig = "yolov5"
        path_weightfile = "yolov5\\weights\\best.pt"  # or any custom trained model
        model = yolov5.load(path_weightfile)

        model.conf = settings.MODEL_CONFIDENCE
        yolo_model_name = self.request.POST.get("yolo_model")
        # classnames = model.names  #(display classes in the model)

        results = model(img, size=416)
        results_list = results.pandas().xyxy[0].to_json(orient="records")
        results_list = literal_eval(results_list)
        
        classes_name_list = [item["name"] for item in results_list]
        # class_num_list = [item["class"] for item in results_list]
        # results_counter = collections.Counter(class_num_list)
        
        
        if results_list == []:
            messages.warning(
            request, f'Model unable to predict. Try with another model.')
        else:
            results.render()
            media_folder = settings.MEDIA_ROOT
            inferenced_img_dir = os.path.join(
                    media_folder, "inferenced_image")
            if not os.path.exists(inferenced_img_dir):
                os.makedirs(inferenced_img_dir)
                    
            # Create/update the inferencedImage instance
            inf_img_qs,created = InferencedImage.objects.get_or_create(
                    orig_image=uploaded_img_qs,
                    inf_image_path=f"{settings.MEDIA_URL}inferenced_image/{uploaded_img_qs}",
                )
            inf_img_qs.detection_info = results_list
            inf_img_qs.model_conf = model.conf

            inf_img_qs.yolo_model = yolo_model_name
            inf_img_qs.save()
        torch.cuda.empty_cache()
            
        # results = model(img, size=416)
        results.render()
        results.print()
        results.pandas().xyxy[0]
        results.save()
        for img in results.ims:
            img_base64 = I.fromarray(img)
            img_base64.save(f"{inferenced_img_dir}/{uploaded_img_qs}", format="PNG")
            
        inference_img = f"{settings.MEDIA_URL}inferenced_image/{uploaded_img_qs}"
   
        carinfo.carName = classes_name_list
    
        #머신러닝 모델 가져오기
        car_learn = joblib.load('pkl\saved_model.pkl')
        car = car_learn.predict([[car_year,request.POST['carDistance'],request.POST['carFuel'],results_list[0]['class']]])
        carinfo.carprice = car # 차량 중고가
        carinfo.save()
        
        return redirect(reverse('carSearch:carList'))

def carList(request):
    form = CarInfo.objects.filter().last()
    uploaded_img_qs = ImageModel.objects.filter().last()
    inference_img = f"{settings.MEDIA_URL}inferenced_image/{uploaded_img_qs}"
    
    context = {
        "file":form,
        "image":uploaded_img_qs,
        "inf_image":inference_img
    }
    return render(request,'carSearchSite/carlist.html',context)

def deleteInfo(request,deleteqs,deleteimg):
    image = ImageModel.objects.get(id=deleteimg)
    qs = CarInfo.objects.get(id=deleteqs)
    
    media_root = settings.MEDIA_ROOT
    print('media_root:%s' % media_root)

    
    deleteimage = f"{media_root}\images\{image}"
    deleteInferenced = f"{media_root}\inferenced_image\{image}"
    
    print('deleteimage:%s' % deleteimage)
    print('deleteInferenced:%s' % deleteInferenced)
         
    #실제 파일 삭제를 위한 코드
    if os.path.isfile(deleteimage):
        os.remove(deleteimage) #실제 파일 삭제
       
    if os.path.isfile(deleteInferenced):
        os.remove(deleteInferenced) #실제 파일 삭제
         
    #DB에서 해당 정보 삭제  
    qs.delete()
    image.delete()
    
    return redirect(reverse("carSearch:FP"))
    

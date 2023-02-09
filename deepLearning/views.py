import os
import io
from PIL import Image as I
import torch
from ast import literal_eval
import yolov5
import collections

from django.shortcuts import render
from django.views.generic import CreateView #ListView, DetailView, DeleteView, UpdateView
from django.contrib import messages
from django.conf import settings

from deepLearning.models import InferencedImage
from deepLearning.models import ImageModel
from deepLearning.forms import ImageUploadForm

def deepLearning(request):
    return render(request,'deepLearning/imagemodel_form.html')


class UploadImage(CreateView):
    model = ImageModel
    template_name = 'deepLearning/imagemodel_form.html'
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            img = request.FILES.get('image')
            
            # 이미지 모델의 인스턴스
            img_instance = ImageModel(image=img) 
            img_instance.save()
            
            # 제일 최근에 업로드한 겍체의 쿼리셋 확인
            uploaded_img_qs = ImageModel.objects.filter().last()
            
            # byte로 환산 후 이미지 오픈
            img_bytes = uploaded_img_qs.image.read()
            img = I.open(io.BytesIO(img_bytes))
            
            # 학습된 욜로 모델 경로(설명)
            path_weightfile = "yolov5\\weights\\best.pt"  # 커스텀 yolov5 weights 모델
            #path_hubconfig = "yolov5"
            # model = torch.hub.load(path_hubconfig, 'custom', path=path_weightfile, source='local')
            
            # 욜로 생성(detect)
            model = yolov5.load(path_weightfile)
            # 율로 모델 셋팅 (컨피던스값 셋팅)
            model.conf = settings.MODEL_CONFIDENCE
            # 욜로 모델 이름
            yolo_model_name = self.request.POST.get("yolo_model")
            # classnames = model.names  # 차량 종류 보여줄수 있는 변수
            
            #욜로 모델 학습(이미지 크기 설정)
            results = model(img, size=416)
            
            #예측한 결과가 json 형태로 저장
            results_list = results.pandas().xyxy[0].to_json(orient="records")
            
            results_list = literal_eval(results_list)   # 탐지된 개수만큼의 Bbox 정보와 차종 분류 정보가 담겨있는 리스트
            class_num_list = [item["class"] for item in results_list]    # 탐지된 개수만큼의 차종 클라스 번호 리스트
            class_name_list = [item["name"] for item in results_list]    # 탐지된 개수만큼의 차종 이름 리스트
            results_counter = collections.Counter(class_num_list) # 
            
            # 탐지된 차종이 없을때
            if results_list == []: 
                messages.warning(
                request, f'Model unable to predict. Try with another model.')
            
            # 탐지된 차종이 있을때
            else:
                results.render() # 이미지 렌더링
                
                 # 예측한 이미지의 파일폴더 생성
                media_folder = settings.MEDIA_ROOT
                inferenced_img_dir = os.path.join(
                        media_folder, "inferenced_image")
                if not os.path.exists(inferenced_img_dir):
                    os.makedirs(inferenced_img_dir)
                        
                # 라벨링 된 bbox가 있는 사진 객체 InferencedImage 생성 또는 최신화
                inf_img_qs, created = InferencedImage.objects.get_or_create(
                        orig_image=uploaded_img_qs,
                        inf_image_path=f"{settings.MEDIA_URL}inferenced_image/{uploaded_img_qs}",
                    )
                
                #데이터베이스 저장
                inf_img_qs.detection_info = results_list
                inf_img_qs.model_conf = model.conf

                inf_img_qs.yolo_model = yolo_model_name
                inf_img_qs.save()
                
                
            torch.cuda.empty_cache()
            # print(dir(results))
            results.render()
            results.print()
            results.pandas().xyxy[0]
            results.save()
            
            
            for img in results.ims:
                img_base64 = I.fromarray(img)
                img_base64.save(f"{inferenced_img_dir}/{uploaded_img_qs}", format="PNG")
                
            inference_img = f"{settings.MEDIA_URL}inferenced_image/{uploaded_img_qs}"
            
            inf_img_qs = InferencedImage.objects.get(orig_image=uploaded_img_qs)

            form = ImageUploadForm()
            context = {
                "form": form,
                "inference_img": inference_img,
                "img_qs": uploaded_img_qs,
                "results_list": results_list,
                "inf_img_qs": inf_img_qs,
                "class_num_list": class_num_list,
                "class_name_list": class_name_list,
                "results_counter": results_counter,
            }
            return render(request, 'deepLearning/imagemodel_form.html', context)

        else:
            form = ImageUploadForm()
            context = {
                "form": form
            }
            return render(request, 'deepLearning/imagemodel_form.html', context)


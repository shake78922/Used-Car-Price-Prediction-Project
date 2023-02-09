from django.shortcuts import render,redirect, reverse
from django.views.generic import View
from pathlib import Path
import os
import pandas as pd

from machineLearning.models import CarInfo
from machineLearning.forms import CarInfoForm

from django.conf import settings
from django.utils.dateformat import DateFormat
from datetime import datetime
import joblib 
# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent
metacsv_path = os.path.join(BASE_DIR/"static"/"machineLearning"/"kcar_meta.csv")
machine_path = os.path.join(BASE_DIR/"pkl"/"saved_model.pkl")

class CarSearch(View):
    def get(self,request):
        form = CarInfoForm()
        context = {
            'form':form
        }
        return render(request,"machineLearning/KO.html",context)

    def post(self,request):     
        # 메타csv에서 차종류 받아오기
        df = pd.read_csv(metacsv_path, index_col=0, encoding='euc-kr')
        car_list=list(df['class_names'])
        
        #차 클래스
        car_class = request.POST['car_class']

        class_num = car_list.index(car_class)
           
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
        carinfo.carName = request.POST['car_class'] # 차량 이름
        carinfo.carCalendar = request.POST['carCalendar'] # 차량 연식
        carinfo.carDistance = request.POST['carDistance'] # 차량 주행거리
        carinfo.carFuel = request.POST['carFuel'] # 차량 연료
       
        carinfo.carYear = year
        carinfo.carMonth = month
        carinfo.carModel = car_year
       
        
        #머신러닝 모델 가져오기
        car_learn = joblib.load(machine_path)
        car = car_learn.predict([[car_year,request.POST['carDistance'],request.POST['carFuel'], class_num]])
        carinfo.carprice = car # 차량 중고가
        carinfo.save()
        
        return redirect(reverse('machineLearning:result'))
    
    
def result(request):
    carinfo = CarInfo.objects.filter().last()
    context = {
        "carinfo":carinfo
    }
    
    return render(request, 'machineLearning/result.html',context)






# def main(request):
#     df = pd.read_csv(metacsv_path, index_col=0, encoding='euc-kr')
#     car_list=list(df['class_names'])
#     print(car_list)
#     print(request.POST)
#     return render(request,"KO/KO.html")

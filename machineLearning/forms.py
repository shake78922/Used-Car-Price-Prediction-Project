from django import forms
from machineLearning.models import CarInfo

class CarInfoForm(forms.ModelForm):
    class Meta:
        model = CarInfo
        fields = ['carCalendar','carDistance','carFuel']
        widgets = {
            'carCalendar' : forms.DateInput(
                format=('%Y/%m/%/d'),
                attrs={'placeholder':'날짜를 입력해주세요',
                       'type':'date'}
                )
        }
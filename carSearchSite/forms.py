from django import forms
from carSearchSite.models import CarInfo,ImageModel

class CarInfoForm(forms.ModelForm):
    class Meta:
        model = CarInfo
        fields = ['carCalendar','carDistance','carFuel']
        widgets = {
            'carCalendar' : forms.DateInput(
                format=('%Y/%m/%/d'),
                attrs={'class': "form-control",
                       'placeholder':'날짜를 입력해주세요',
                       'type':'date',
                       'style': 'max-width: 300px;'
                       }
                ),
            
            'carDistance' : forms.NumberInput(
                attrs={'class': "form-control",
                       'style': 'max-width: 300px;'
                      }
            ),
            
            'carFuel' : forms.Select(
                attrs={'style': 'max-width: 300px; text-align: center',
                       'class': "form-control"
                      }
            )
        }
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image']
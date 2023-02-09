from django.db import models

# Create your models here.
class CarInfo(models.Model):
    

    fuel_type = [
        (0,'CNG'), 
        (1,'LPG(일반인 구입)'), 
        (2,'LPG+전기'), 
        (3,'가솔린'), 
        (4,'가솔린+CNG'), 
        (5,'가솔린+LPG'), 
        (6,'가솔린+전기'), 
        (7,'디젤'), 
        (8,'수소'),
        (9,'전기')
    ]
    

    # carImage = models.ImageField(null=False,upload_to="",verbose_name="car")

    carName = models.CharField(null=True,max_length=150,verbose_name='name')
    carCalendar = models.DateField(null=True,verbose_name="calendar")
    carYear = models.IntegerField(null=True,default=0,verbose_name='year')
    carMonth = models.IntegerField(null=True,default=0,verbose_name='month')
    carModel = models.IntegerField(null=True,default=0,verbose_name='yearlyModel')
    
    carDistance = models.IntegerField(default=0,null=True,verbose_name='distance')
    carFuel = models.IntegerField(null=True,choices=fuel_type,verbose_name='fuel')
    carprice = models.IntegerField(null=False,verbose_name='price')
    
    
    def __str__(self) -> str:
        return "{}".format(self.carImage)
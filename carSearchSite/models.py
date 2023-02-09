from django.db import models

from mysite.models import CreationModificationDateBase
from django.utils.translation import gettext_lazy as _

import os

# Create your models here.


#딥 러닝 모델
class InferencedImage(CreationModificationDateBase):
    orig_image = models.ForeignKey(
        "ImageModel",
        on_delete=models.CASCADE,
        related_name="detectedimages",
        help_text="Main Image",
        null=True,
        blank=True
    )

    inf_image_path = models.CharField(max_length=250,
                                      null=True,
                                      blank=True
                                      )
    
    detection_info = models.JSONField(null=True, blank=True)

    YOLOMODEL_CHOICES = [
        ('best.pt', 'best.pt'),
        ('last.pt', 'last.pt'),
    ]

    yolo_model = models.CharField(_('YOLOV5 Models'),
                                  max_length=250,
                                  null=True,
                                  blank=True,
                                  choices=YOLOMODEL_CHOICES,
                                  default=YOLOMODEL_CHOICES[0],
                                  help_text="Selected yolo model will download. \
                                 Requires an active internet connection."
                                  )

    model_conf = models.DecimalField(_('Model confidence'),
                                     decimal_places=2,
                                     max_digits=4,
                                     null=True,
                                     blank=True)

#이미지 저장 
class ImageModel(models.Model):
    name = models.CharField(_('Image Name'), max_length=150, null=True)
    image = models.ImageField(_("image"), upload_to='images')

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self) -> str:
        return str(os.path.split(self.image.path)[-1])
    
#차량 정보
class CarInfo(models.Model):
    fue_type = [
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
    carName = models.CharField(null=True,default="",max_length=200,verbose_name="car")
    carCalendar = models.DateField(null=True,verbose_name="calendar")
    carYear = models.IntegerField(null=True,default=0,verbose_name='year')
    carMonth = models.IntegerField(null=True,default=0,verbose_name='month')
    carModel = models.IntegerField(null=True,default=0,verbose_name='yearlyModel')
    
    carDistance = models.IntegerField(default=0,null=True,verbose_name='distance')
    carFuel = models.IntegerField(null=True,choices=fue_type,verbose_name='fuel')
    carprice = models.IntegerField(null=False,verbose_name='price')

    def __str__(self) -> str:
        return "{}".format(self.carCalendar)


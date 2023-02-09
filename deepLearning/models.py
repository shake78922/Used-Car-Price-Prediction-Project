import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_image_file_extension

from mysite.models import CreationModificationDateBase

# 딥러닝 모델 처리후 저장될 모델
class InferencedImage(CreationModificationDateBase):
    
    # 이미지 저장 모델 외래키
    orig_image = models.ForeignKey(
        "ImageModel",
        on_delete=models.CASCADE,
        related_name="detectedimages",
        help_text="Main Image",
        null=True,
        blank=True
    )

    # 모델 작동했을때, 분석된 이미지 저장될 경로(타입 : string)
    inf_image_path = models.CharField(max_length=250,
                                      null=True,
                                      blank=True
                                      )
    
    # 율로 작동한 후, 율로모델에 대한 바운딩box 정보 (x,y,width,height,classNum,className)
    detection_info = models.JSONField(null=True, blank=True)

    # 사용 가능한 율로 모델
    YOLOMODEL_CHOICES = [
        ('best.pt', 'best.pt'),
        ('last.pt', 'last.pt'),
    ]

    # 율로 모델(weight 파일)
    yolo_model = models.CharField(_('YOLOV5 Models'),
                                  max_length=250,
                                  null=True,
                                  blank=True,
                                  choices=YOLOMODEL_CHOICES,
                                  default=YOLOMODEL_CHOICES[0],
                                  help_text="Selected yolo model will download. \
                                 Requires an active internet connection."
                                  )
    # 율로 모델의 정확도(신빙성) --> 모델이 이미지를 얼마나 잘 인지하는지
    model_conf = models.DecimalField(_('Model confidence'),
                                     decimal_places=2,
                                     max_digits=4,
                                     null=True,
                                     blank=True)


# 업로드하는 이미지 저장모델
class ImageModel(models.Model):
    
    image = models.ImageField(_("image"), upload_to='images') #사진
    name = models.CharField(_('Image Name'), max_length=150, null=True) #이름
    
    
    class Meta:
        verbose_name = "Image" # 사진 한장
        verbose_name_plural = "Images" # 다량의 사진

    def __str__(self):
        return str(os.path.split(self.image.path)[-1])



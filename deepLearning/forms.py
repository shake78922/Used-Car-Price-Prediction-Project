from django import forms
from deepLearning.models import ImageModel

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image']
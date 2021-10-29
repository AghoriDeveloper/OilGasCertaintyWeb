from django.forms import ModelForm
from .models import ObjAModel


class ObjAForm(ModelForm):
    class Meta:
        model = ObjAModel
        fields = '__all__'

from django.forms import ModelForm
from .models import ObjCModel


class ObjCForm(ModelForm):
    class Meta:
        model = ObjCModel
        fields = '__all__'

from django.forms import ModelForm
from .models import ObjABCModel


class ObjABCForm(ModelForm):
    class Meta:
        model = ObjABCModel
        fields = '__all__'

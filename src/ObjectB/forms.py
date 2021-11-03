from django.forms import ModelForm
from .models import ObjBModel


class ObjBForm(ModelForm):
    class Meta:
        model = ObjBModel
        fields = '__all__'

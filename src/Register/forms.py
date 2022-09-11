from django.forms import ModelForm
from .models import RegisterModel


class RegisterForm(ModelForm):
    class Meta:
        model = RegisterModel
        fields = '__all__'

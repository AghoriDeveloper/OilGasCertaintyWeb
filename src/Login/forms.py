from django.forms import ModelForm
from .models import LoginModel


class LoginForm(ModelForm):
    class Meta:
        model = LoginModel
        fields = '__all__'

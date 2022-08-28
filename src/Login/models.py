from django.db import models

class LoginModel(models.Model):
    email = models.CharField(max_length=200, blank=False, null=False)
    password = models.CharField(max_length=200, blank=False, null=False)

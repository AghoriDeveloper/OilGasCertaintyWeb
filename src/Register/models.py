from django.db import models

class RegisterModel(models.Model):
    email = models.CharField(max_length=200, blank=False, null=False)
    password = models.CharField(max_length=200, blank=False, null=False)
    password2 = models.CharField(max_length=200, blank=False, null=False)

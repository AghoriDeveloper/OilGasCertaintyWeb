from django.db import models

class RegisterModel(models.Model):
    email = models.CharField(max_length=200, blank=False, null=False)
    password = models.CharField(max_length=200, blank=False, null=False)
    password2 = models.CharField(max_length=200, blank=False, null=False)
    obja = models.BooleanField(default=False, blank=False, null=False)
    objb = models.BooleanField(default=False, blank=False, null=False)
    objc = models.BooleanField(default=False, blank=False, null=False)
    objabc = models.BooleanField(default=False, blank=False, null=False)

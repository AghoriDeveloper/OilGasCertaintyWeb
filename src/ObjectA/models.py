from django.db import models

class ObjAModel(models.Model):

    prodType = models.CharField(max_length=200)
    threshold = models.CharField(max_length=200)
    curveType = models.CharField(max_length=200)
    excelFile = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

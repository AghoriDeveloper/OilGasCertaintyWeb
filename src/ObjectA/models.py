from django.db import models


class ObjAModel(models.Model):
    prodType = models.CharField(max_length=200, blank=False, null=False)
    threshold = models.FloatField(blank=False, null=False)
    curveType = models.CharField(max_length=200, blank=False, null=False)
    fileA = models.FileField(upload_to='media', default='media/declinecurve_input.xlsx', blank=False, null=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

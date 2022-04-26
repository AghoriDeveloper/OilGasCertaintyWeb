from django.db import models

class ObjBModel(models.Model):
    oilPrice = models.FloatField(blank=False, null=False)
    oilSD = models.FloatField(blank=False, null=False)
    gasPrice = models.FloatField(blank=False, null=False)
    gasSD = models.FloatField(blank=False, null=False)
    percLine = models.FloatField(blank=False, null=False)

    def __str__(self):
        return self.oilPrice + ' ' + self.gasPrice

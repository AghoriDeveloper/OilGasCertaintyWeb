from django.db import models

class ObjBModel(models.Model):
    oilPrice = models.FloatField()
    oilSD = models.FloatField()
    gasPrice = models.FloatField()
    gasSD = models.FloatField()
    percLine = models.FloatField()

    def __str__(self):
        return self.oilPrice + ' ' + self.gasPrice

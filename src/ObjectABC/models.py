from django.db import models

class ObjABCModel(models.Model):
    oilPrice = models.IntegerField()
    oilSD = models.IntegerField()
    gasPrice = models.IntegerField()
    gasSD = models.IntegerField()
    percLine = models.IntegerField()

    def __str__(self):
        return self.oilPrice + ' ' + self.gasPrice

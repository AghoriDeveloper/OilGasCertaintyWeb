from django.db import models

class ObjABCModel(models.Model):
    product = models.CharField(max_length=125)

    scf_bo = models.FloatField()
    bc_mmscfg = models.FloatField()

    oilPrice = models.FloatField()
    oilSD = models.FloatField()
    gasPrice = models.FloatField()
    gasSD = models.FloatField()
    oilPerc = models.FloatField()
    gasPerc = models.FloatField()

    royalty = models.FloatField()
    priceUC = models.CharField(max_length=125)

    fixedCost = models.FloatField()
    indProdCost = models.FloatField()
    oilProdCost = models.FloatField()
    gasProdCost = models.FloatField()

    outputExcelFile = models.CharField(max_length=200)
    hedgedExcelFile = models.CharField(max_length=200)


    def __str__(self):
        return self.oilPrice + ' ' + self.gasPrice

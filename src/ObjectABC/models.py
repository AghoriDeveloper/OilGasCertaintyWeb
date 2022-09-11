from django.db import models

class ObjABCModel(models.Model):
    product = models.CharField(default="oil", max_length=200, blank=False, null=False)
    threshold = models.FloatField(default=1.0, blank=False, null=False)
    bc_mmscfg = models.FloatField(default=1.0, blank=True, null=True)
    gor = models.FloatField(default=1.0, blank=True, null=True)
    curveType = models.CharField(default="hyperbolic", max_length=200, blank=False, null=False)

    excelInput = models.FileField(upload_to='media', default='media/declinecurve_input.xlsx', blank=False, null=False)
    hedgedFileInput = models.FileField(upload_to='media', default='media/expense_hedged_input.xlsx', blank=False, null=False)

    oilPrice = models.FloatField(default=1.0, blank=False, null=False)
    oilSD = models.FloatField(default=1.0, blank=False, null=False)
    gasPrice = models.FloatField(default=1.0, blank=False, null=False)
    gasSD = models.FloatField(default=1.0, blank=False, null=False)

    royalty = models.FloatField(blank=False, null=False)
    priceUC = models.CharField(max_length=125, blank=False, null=False)

    fixedCost = models.FloatField(default=1.0, blank=False, null=False)
    indProdCost = models.FloatField(default=1.0, blank=False, null=False)
    oilProdCost = models.FloatField(default=1.0, blank=False, null=False)
    gasProdCost = models.FloatField(default=1.0, blank=False, null=False)
    costBelowPerc = models.FloatField(default=1.0, blank=False, null=False)
    indProdSD = models.FloatField(default=1.0, blank=False, null=False)

    def __str__(self):
        return self.oilPrice + ' ' + self.gasPrice

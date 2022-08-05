from django.db import models

class ObjCModel(models.Model):
    product = models.CharField(default="oil", max_length=200, blank=False, null=False)
    threshold = models.FloatField(blank=False, null=False)
    bc_mmscfg = models.FloatField(default=1.0, blank=True, null=True)
    gor = models.FloatField(default=1.0, blank=True, null=True)
    curveType = models.CharField(default="hyperbolic", max_length=200, blank=False, null=False)
    excelInput = models.FileField(upload_to='media', default='media/declinecurve_input.xlsx', blank=False, null=False)

    fixedCost = models.FloatField(blank=False, null=False)
    indProdCost = models.FloatField(blank=False, null=False)
    oilProdCost = models.FloatField(blank=False, null=False)
    gasProdCost = models.FloatField(blank=False, null=False)

    costBelowPerc = models.FloatField(blank=False, null=False)
    indProdSD = models.FloatField(blank=False, null=False)

    def __str__(self):
        return self.gor + ' ' + self.bc_mmscfg

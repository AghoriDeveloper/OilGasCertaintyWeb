from django.db import models

class ObjCModel(models.Model):
    threshold = models.FloatField(blank=False, null=False)
    curveType = models.CharField(default="hyperbolic", max_length=200, blank=False, null=False)
    fileA = models.FileField(upload_to='media', default='media/declinecurve_input.xlsx', blank=False, null=False)

    fixedCost = models.FloatField(blank=False, null=False)
    indProdCost = models.FloatField(blank=False, null=False)
    oilProdCost = models.FloatField(blank=False, null=False)
    gasProdCost = models.FloatField(blank=False, null=False)

    costBelowPerc = models.FloatField(blank=False, null=False)
    indProdSD = models.FloatField(blank=False, null=False)

    def __str__(self):
        return self.scf_bo + ' ' + self.bc_mmscfg

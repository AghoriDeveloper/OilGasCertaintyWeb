from django.db import models

class ObjABCModel(models.Model):
    product = models.CharField(max_length=125, blank=False, null=False)

    prod_percentile = models.FloatField(default=60, blank=False, null=False)
    scf_bo = models.FloatField(blank=True, null=True)
    bc_mmscfg = models.FloatField(blank=True, null=True)

    oilPrice = models.FloatField(blank=False, null=False)
    oilSD = models.FloatField(blank=False, null=False)
    gasPrice = models.FloatField(blank=False, null=False)
    gasSD = models.FloatField(blank=False, null=False)
    oilPerc = models.FloatField(blank=False, null=False)
    gasPerc = models.FloatField(blank=False, null=False)

    royalty = models.FloatField(blank=False, null=False)
    priceUC = models.CharField(max_length=125, blank=False, null=False)

    fixedCost = models.FloatField(blank=False, null=False)
    indProdCost = models.FloatField(blank=False, null=False)
    oilProdCost = models.FloatField(blank=False, null=False)
    gasProdCost = models.FloatField(blank=False, null=False)

    outputFileInput = models.FileField(upload_to='media', default='media/expense_declinedcurve_input.xlsx', blank=False, null=False)
    hedgedFileInput = models.FileField(upload_to='media', default='media/expense_hedged_input.xlsx', blank=False, null=False)

    def __str__(self):
        return self.oilPrice + ' ' + self.gasPrice

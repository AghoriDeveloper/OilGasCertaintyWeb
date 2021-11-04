from django.shortcuts import render
from .forms import ObjABCForm
from .processing import setObjecABCValues


def index(request):
    objabc = ObjABCForm()

    if request.method == 'POST':
        objabc = ObjABCForm(request.POST)
        # print(objabc)
        if objabc.is_valid():
            setObjecABCValues(objabc['product'].value(), objabc['scf_bo'].value(), objabc['bc_mmscfg'].value(), objabc['oilPrice'].value(), objabc['oilSD'].value(), objabc['gasPrice'].value(), objabc['gasSD'].value(), objabc['oilPerc'].value(), objabc['gasPerc'].value(), objabc['royalty'].value(), objabc['priceUC'].value(), objabc['fixedCost'].value(), objabc['indProdCost'].value(), objabc['oilProdCost'].value(), objabc['gasProdCost'].value(), objabc['outputExcelFile'].value(), objabc['hedgedExcelFile'].value())
            objabc.save()

    return render(request, "ObjectABC/index.html", {'form': objabc})

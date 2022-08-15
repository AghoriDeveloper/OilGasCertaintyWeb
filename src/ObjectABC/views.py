from django.shortcuts import render
from .forms import ObjABCForm
from .processing import setObjecABCValues


def index(request):
    objabc = ObjABCForm()

    if request.method == 'POST':
        objabc = ObjABCForm(request.POST)
        if objabc.is_valid():
            import_file_path1 = request.FILES['excelInput']
            import_file_path2 = request.FILES['hedgedFileInput']

            response = setObjecABCValues(objabc['product'].value(), objabc['threshold'].value(), objabc['bc_mmscfg'].value(), objabc['gor'].value(), objabc['curveType'].value(), objabc['oilPrice'].value(), objabc['oilSD'].value(), objabc['gasPrice'].value(), objabc['gasSD'].value(), objabc['oilPerc'].value(), objabc['gasPerc'].value(), objabc['royalty'].value(), objabc['priceUC'].value(), objabc['fixedCost'].value(), objabc['indProdCost'].value(), objabc['oilProdCost'].value(), objabc['gasProdCost'].value(), objabc['costBelowPerc'].value(), objabc['indProdSD'].value(), import_file_path1, import_file_path2)
            return response
            objabc.save()

    return render(request, "ObjectABC/index.html", {'form': objabc})

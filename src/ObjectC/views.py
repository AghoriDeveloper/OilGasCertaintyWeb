from django.shortcuts import render
from .forms import ObjCForm
from .processing import setObjecCValues


def index(request):
    objc = ObjCForm()

    if request.method == 'POST':
        objc = ObjCForm(request.POST)
        if objc.is_valid():
            import_file_path = request.FILES['excelInput']
            response = setObjecCValues(objc['threshold'].value(), objc['curveType'].value(), import_file_path, objc['fixedCost'].value(), objc['indProdCost'].value(), objc['oilProdCost'].value(), objc['gasProdCost'].value(), objc['costBelowPerc'].value(), objc['indProdSD'].value())
            return response
            objc.save()

    return render(request, "ObjectC/index.html", {'form': objc})

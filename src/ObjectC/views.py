from django.shortcuts import render
from .forms import ObjCForm
from .processing import setObjecCValues


def index(request):
    objc = ObjCForm()

    if request.method == 'POST':
        objc = ObjCForm(request.POST)
        if objc.is_valid():
            import_file_path = request.FILES['excelInput']
            response = setObjecCValues(objc['product'].value(), objc['threshold'].value(), objc['bc_mmscfg'].value(), objc['gor'].value(), objc['curveType'].value(), import_file_path, objc['fixedCost'].value(), objc['indProdCost'].value(), objc['oilProdCost'].value(), objc['gasProdCost'].value(), objc['costBelowPerc'].value(), objc['indProdSD'].value())
            return response
            objc.save()

    if request.session['objc'] == 1:
        return render(request, "ObjectC/index.html", {'form': objc})
    else:
        raise Http404

from django.shortcuts import render
from .forms import ObjAForm
from .processing import setObjecAValues


def index(request):
    obja = ObjAForm()

    if request.method == 'POST':
        obja = ObjAForm(request.POST)
        if obja.is_valid():
            import_file_path = request.FILES['excelInput']

            chart, threshold = setObjecAValues(obja['prodType'].value(), obja['threshold'].value(), obja['curveType'].value(), import_file_path)
            obja.save()

            return render(request, "ObjectA/chart.html", {'chart': chart, 'threshold': threshold})

    return render(request, "ObjectA/index.html", {'form': obja})

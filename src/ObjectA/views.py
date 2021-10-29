from django.shortcuts import render
from .forms import ObjAForm
from .processing import setObjecAValues


def index(request):
    obja = ObjAForm()

    if request.method == 'POST':
        obja = ObjAForm(request.POST)
        if obja.is_valid():
            # print(obja)
            # print(obja['prodType'].value())
            # print(obja['threshold'].value())
            # print(obja['curveType'].value())
            # print(obja['excelFile'].value())

            chart = setObjecAValues(obja['prodType'].value(), obja['threshold'].value(), obja['curveType'].value(), obja['excelFile'].value())
            obja.save()

            return render(request, "ObjectA/chart.html", {'chart': chart})

    return render(request, "ObjectA/index.html", {'form': obja})

from django.shortcuts import render
from .forms import ObjABCForm
from .processing import setObjecABCValues


def index(request):
    objabc = ObjABCForm()

    if request.method == 'POST':
        objabc = ObjABCForm(request.POST)
        if objabc.is_valid():
            print(objabc)

            chart = setObjecABCValues(objabc['oilPrice'].value(), objabc['oilSD'].value(), objabc['gasPrice'].value(),
                                      objabc['gasSD'].value(), objabc['percLine'].value())
            objabc.save()

            return render(request, "ObjectABC/chart.html", {'chart': chart})

    return render(request, "ObjectABC/index.html", {'form': objabc})

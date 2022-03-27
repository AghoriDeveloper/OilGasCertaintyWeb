from django.shortcuts import render
from .forms import ObjBForm
from .processing import setObjecBValues


def index(request):
    objb = ObjBForm()

    if request.method == 'POST':
        objb = ObjBForm(request.POST)
        if objb.is_valid():
            print(objb)

            chartoil, chartgas, chartoillist, chartgaslist = setObjecBValues(objb['oilPrice'].value(), objb['oilSD'].value(), objb['gasPrice'].value(), objb['gasSD'].value(), objb['percLine'].value())
            objb.save()

            return render(request, "ObjectB/chart.html", {'chartoil': chartoil, 'chartgas': chartgas, 'chartoillist': chartoillist, 'chartgaslist': chartgaslist})

    return render(request, "ObjectB/index.html", {'form': objb})

from django.shortcuts import render
from .forms import ObjBForm
from .processing import setObjecBValues


def index(request):
    objb = ObjBForm()

    if request.method == 'POST':
        objb = ObjBForm(request.POST)
        if objb.is_valid():
            print(objb)

            chart = setObjecBValues(objb['oilPrice'].value(), objb['oilSD'].value(), objb['gasPrice'].value(), objb['gasSD'].value(), objb['percLine'].value())
            objb.save()

            return render(request, "ObjectB/chart.html", {'chart': chart})

    return render(request, "ObjectB/index.html", {'form': objb})

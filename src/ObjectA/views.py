from django.shortcuts import render
from .forms import ObjAForm
from .processing import setObjecAValues
from tkinter import filedialog
import tkinter as tk


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

            root = tk.Tk()
            root.title("Select Excel File")
            root.attributes("-topmost", True)
            root.withdraw()
            import_file_path = filedialog.askopenfilename()
            print(import_file_path)
            root.destroy()

            # chart = setObjecAValues(obja['prodType'].value(), obja['threshold'].value(), obja['curveType'].value(), obja['excelFile'].value())
            chart, threshold = setObjecAValues(obja['prodType'].value(), obja['threshold'].value(), obja['curveType'].value(), import_file_path)
            obja.save()

            return render(request, "ObjectA/chart.html", {'chart': chart, 'threshold': threshold})

    return render(request, "ObjectA/index.html", {'form': obja})

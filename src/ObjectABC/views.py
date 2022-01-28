from django.shortcuts import render
from .forms import ObjABCForm
from .processing import setObjecABCValues
from tkinter import filedialog
import tkinter as tk


def index(request):
    objabc = ObjABCForm()

    if request.method == 'POST':
        objabc = ObjABCForm(request.POST)
        print(objabc)
        if objabc.is_valid():
            root = tk.Tk()
            root.title("Select Excel File")
            root.attributes("-topmost", True)
            root.withdraw()
            import_file_path1 = filedialog.askopenfilename()
            print(import_file_path1)

            import_file_path2 = filedialog.askopenfilename()
            print(import_file_path2)
            root.destroy()

            setObjecABCValues(objabc['product'].value(), objabc['scf_bo'].value(), objabc['bc_mmscfg'].value(), objabc['oilPrice'].value(), objabc['oilSD'].value(), objabc['gasPrice'].value(), objabc['gasSD'].value(), objabc['oilPerc'].value(), objabc['gasPerc'].value(), objabc['royalty'].value(), objabc['priceUC'].value(), objabc['fixedCost'].value(), objabc['indProdCost'].value(), objabc['oilProdCost'].value(), objabc['gasProdCost'].value(), import_file_path1, import_file_path2)
            objabc.save()

    return render(request, "ObjectABC/index.html", {'form': objabc})

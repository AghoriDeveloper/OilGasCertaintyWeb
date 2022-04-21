import io
import os

import xlsxwriter
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ObjAForm
from .processing import setObjecAValues

Excel_input = []

def index(request):
    global Excel_input
    obja = ObjAForm()

    if request.method == 'POST':
        obja = ObjAForm(request.POST)
        if obja.is_valid():
            import_file_path = request.FILES['excelInput']

            chart, threshold, Excel_input = setObjecAValues(obja['prodType'].value(), obja['threshold'].value(), obja['curveType'].value(), import_file_path)
            obja.save()

            return render(request, "ObjectA/chart.html", {'chart': chart, 'threshold': threshold})

    return render(request, "ObjectA/index.html", {'form': obja})


def downloadexcel(request):
    global Excel_input
    T_ext = Excel_input[0]
    Q_Pred = Excel_input[1]
    pred = Excel_input[2]
    Threshold = Excel_input[3]

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Declined Curve")

    worksheet.write(0, 0, "Month")
    worksheet.write(0, 1, "Predicted Price")
    worksheet.write(0, 2, str(Threshold) + "% Confident Value")

    for i in range(len(T_ext)):
        worksheet.write(i + 1, 0, T_ext[i])
    for i in range(len(Q_Pred)):
        worksheet.write(i + 1, 1, Q_Pred[i])
    for i in range(len(pred)):
        worksheet.write(i + 1, 2, pred[i])

    workbook.close()

    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=Delined_Curve_Output.xlsx"
    output.close()

    return response

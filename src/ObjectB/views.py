import io
import os

import xlsxwriter
import xlwt
from django.http import HttpResponse, Http404
from django.shortcuts import render
from .forms import ObjBForm
from .processing import setObjecBValues

oilPrice, gasPrice, oilStd, gasStd, percentile = 0, 0, 0, 0, 0
chartoil, chartgas, chartoillist, chartgaslist = 0, 0, 0, 0


def index(request):
    global oilPrice, gasPrice, oilStd, gasStd, percentile, chartoil, chartgas, chartoillist, chartgaslist
    objb = ObjBForm()

    if request.method == 'POST':
        objb = ObjBForm(request.POST)
        if objb.is_valid():
            # print(objb)

            oilPrice = objb['oilPrice'].value()
            oilStd = objb['oilSD'].value()
            gasPrice = objb['gasPrice'].value()
            gasStd = objb['gasSD'].value()
            percentile = objb['percLine'].value()

            chartoil, chartgas, chartoillist, chartgaslist = setObjecBValues(oilPrice, oilStd, gasPrice, gasStd, percentile)
            objb.save()

            return render(request, "ObjectB/chart.html", {'chartoil': chartoil, 'chartgas': chartgas, 'chartoillist': chartoillist, 'chartgaslist': chartgaslist})

    if request.session['objb'] == 1:
        return render(request, "ObjectB/index.html", {'form': objb})
    else:
        raise Http404


def downloadexcel(request):
    global oilPrice, gasPrice, oilStd, gasStd, percentile, chartoil, chartgas, chartoillist, chartgaslist

    image_width = 200.0
    image_height = 100.0
    cell_width = 64.0
    cell_height = 20.0
    x_scale = cell_width / image_width
    y_scale = cell_height / image_height

    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Product Price")

    worksheet.set_column(1, 2, 15)
    worksheet.set_column(5, 5, 25)

    worksheet.write(0, 0, "Month")
    worksheet.write(0, 1, "Oil Price ($)")
    worksheet.write(0, 2, "Gas Price ($)")
    
    worksheet.write(2, 5, "Oil Price ($)")
    worksheet.write(3, 5, "Oil Std. Deviation (%)")
    worksheet.write(4, 5, "Gas Price ($)")
    worksheet.write(5, 5, "Gas Std. Deviation (%)")
    worksheet.write(6, 5, "Percentile Line (%)")

    for i in range(len(chartoillist)):
        worksheet.write(i + 1, 0, i)
        worksheet.write(i + 1, 1, chartoillist[i])
        worksheet.write(i + 1, 2, chartgaslist[i])

    worksheet.write(2, 6, oilPrice)
    worksheet.write(3, 6, oilStd)
    worksheet.write(4, 6, gasPrice)
    worksheet.write(5, 6, gasStd)
    worksheet.write(6, 6, percentile)

    worksheet.insert_image('B17', 'Graph/ChartOil.png', {'x_scale': x_scale, 'y_scale': y_scale})
    worksheet.insert_image('G17', 'Graph/ChartGas.png', {'x_scale': x_scale, 'y_scale': y_scale})

    workbook.close()

    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=Product_Price_Output.xlsx"
    output.close()

    return response

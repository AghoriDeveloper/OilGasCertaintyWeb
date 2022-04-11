import io
import os

import xlsxwriter
import xlwt
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ObjBForm
from .processing import setObjecBValues

oilPrice, gasPrice, oilStd, gasStd = 0, 0, 0, 0
chartoil, chartgas, chartoillist, chartgaslist = 0, 0, 0, 0


def index(request):
    global oilPrice, gasPrice, oilStd, gasStd, chartoil, chartgas, chartoillist, chartgaslist
    objb = ObjBForm()

    if request.method == 'POST':
        objb = ObjBForm(request.POST)
        if objb.is_valid():
            # print(objb)

            oilPrice = objb['oilPrice'].value()
            oilStd = objb['oilSD'].value()
            gasPrice = objb['gasPrice'].value()
            gasStd = objb['gasSD'].value()

            chartoil, chartgas, chartoillist, chartgaslist = setObjecBValues(oilPrice, oilStd, gasPrice, gasStd, objb['percLine'].value())
            objb.save()

            return render(request, "ObjectB/chart.html", {'chartoil': chartoil, 'chartgas': chartgas, 'chartoillist': chartoillist, 'chartgaslist': chartgaslist})

    return render(request, "ObjectB/index.html", {'form': objb})


# def downloadexcel(request):
#     global oilPrice, gasPrice, oilStd, gasStd, chartoil, chartgas, chartoillist, chartgaslist
#     response = HttpResponse(content_type='application/ms-excel')
#
#     response['Content-Disposition'] = 'attachment; filename="Product_Price_Output.xls"'
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet("Product_Price")
#
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#
#     ws.col(1).width = 3000
#     ws.col(2).width = 3000
#     ws.col(5).width = 6000
#     oil_columns = ["Month", "Oil Price ($)", "Gas Price ($)"]
#
#     for col_num in range(len(oil_columns)):
#         ws.write(0, col_num, oil_columns[col_num], font_style)
#
#     ws.write(2, 5, "Oil Price ($)", font_style)
#     ws.write(3, 5, "Oil Std. Deviation (%)", font_style)
#     ws.write(4, 5, "Gas Price ($)", font_style)
#     ws.write(5, 5, "Gas Std. Deviation (%)", font_style)
#
#     font_style = xlwt.XFStyle()
#     for i in range(len(chartoillist)):
#         ws.write(i + 1, 0, i, font_style)
#         ws.write(i + 1, 1, chartoillist[i], font_style)
#         ws.write(i + 1, 2, chartgaslist[i], font_style)
#
#     ws.write(2, 6, oilPrice, font_style)
#     ws.write(3, 6, oilStd, font_style)
#     ws.write(4, 6, gasPrice, font_style)
#     ws.write(5, 6, gasStd, font_style)
#
#     wb.save(response)
#     return response


def downloadexcel(request):
    global oilPrice, gasPrice, oilStd, gasStd, chartoil, chartgas, chartoillist, chartgaslist

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

    for i in range(len(chartoillist)):
        worksheet.write(i + 1, 0, i)
        worksheet.write(i + 1, 1, chartoillist[i])
        worksheet.write(i + 1, 2, chartgaslist[i])

    worksheet.write(2, 6, oilPrice)
    worksheet.write(3, 6, oilStd)
    worksheet.write(4, 6, gasPrice)
    worksheet.write(5, 6, gasStd)

    worksheet.insert_image('B17', 'Graph/ChartOil.png', {'x_scale': x_scale, 'y_scale': y_scale})
    worksheet.insert_image('G17', 'Graph/ChartGas.png', {'x_scale': x_scale, 'y_scale': y_scale})

    workbook.close()

    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=Product_Price_Output.xlsx"
    output.close()

    return response



# def downloadexcel(request):
#     global chartoil, chartgas, chartoillist, chartgaslist
#     searchWord = request.POST.get('mybtn2', '')
#
#     workbook = xlsxwriter.Workbook(os.path.expanduser("~") + "/Downloads/" + 'Product_Price_Output.xlsx')
#     oil_worksheet = workbook.add_worksheet("Oil Price")
#     gas_worksheet = workbook.add_worksheet("Gas Price")
#
#     oil_worksheet.write(0, 0, "Month")
#     oil_worksheet.write(0, 1, "Oil Price ($)")
#     gas_worksheet.write(0, 0, "Month")
#     gas_worksheet.write(0, 1, "Gas Price ($)")
#
#     for i in range(len(chartoillist)):
#         oil_worksheet.write(i + 1, 0, i)
#         oil_worksheet.write(i + 1, 1, chartoillist[i])
#         gas_worksheet.write(i + 1, 0, i)
#         gas_worksheet.write(i + 1, 1, chartgaslist[i])
#
#     workbook.close()
#
#     return render(request, "ObjectB/chart.html", {'chartoil': chartoil, 'chartgas': chartgas, 'chartoillist': chartoillist, 'chartgaslist': chartgaslist})

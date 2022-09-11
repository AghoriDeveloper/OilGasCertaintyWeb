import io
import pandas as pd
import numpy as np
from django.http import HttpResponse
from scipy.optimize import curve_fit
import math
import xlsxwriter
import os
from django.conf import settings

Product, Threshold, BC_MMSCFG, GOR, CurveType, OilPrice, OilSD, GasPrice, GasSD, Royalty, PriceUC, FixedCost, InProdCost, OilProdCost, GasProdCost, CostBelowPerc, IndProdSD, ExcelFile, HedgedExcelFile = '', 0, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, '', ''
Chart = -1
Response = -1
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = [], [], [], [], [], [], [], [], [], []
col11, col12, col13, col14, col15, col16, col17, col18, col19, col20 = [], [], [], [], [], [], [], [], [], []
col21, col22, col23, col24, col25 = [], [], [], [], []
percentile = 60.0

def setObjecABCValues(product, threshold, bc_mmscfg, gor, curveType, oilPrice, oilSD, gasPrice, gasSD, royalty, priceUC, fixedCost, indProdCost, oilProdCost, gasProdCost, costBelowPerc, indProdSD, excelFile, hedgedExcelFile):
    global Response, Product, Threshold, BC_MMSCFG, GOR, CurveType, OilPrice, OilSD, GasPrice, GasSD, Royalty, PriceUC, FixedCost, InProdCost, OilProdCost, GasProdCost, CostBelowPerc, IndProdSD, ExcelFile, HedgedExcelFile
    Product = product
    Threshold = threshold
    BC_MMSCFG = bc_mmscfg
    GOR = gor
    CurveType = curveType
    OilPrice = oilPrice
    OilSD = oilSD
    GasPrice = gasPrice
    GasSD = gasSD
    Royalty = royalty
    PriceUC = priceUC
    FixedCost = fixedCost
    InProdCost = indProdCost
    OilProdCost = oilProdCost
    GasProdCost = gasProdCost
    CostBelowPerc = costBelowPerc
    IndProdSD = indProdSD
    ExcelFile = excelFile
    HedgedExcelFile = hedgedExcelFile

    getExcel()
    getDeclineCurveData(threshold, curveType, excelFile)
    create_excel()

    return Response


def getExcel():
    global df, Threshold, percentile, col7, col8, col9, col10, OutputExcelFile, HedgedExcelFile

    import_file_path = HedgedExcelFile
    df_hedged = pd.read_excel(import_file_path)

    col7 = df_hedged.iloc[:, [0]]
    col8 = df_hedged.iloc[:, [1]]
    col9 = df_hedged.iloc[:, [2]]
    col10 = df_hedged.iloc[:, [3]]

    percentile = Threshold


def decline_curve(curve_type, q_i):
    if curve_type == "exponential":
        def exponential_decline(T, a):
            return q_i * np.exp(-a * T)

        return exponential_decline

    elif curve_type == "hyperbolic":
        def hyperbolic_decline(T, a_i, b):
            return q_i / np.power((1 + b * a_i * T), 1. / b)

        return hyperbolic_decline


def getDeclineCurveData(threshold, curveType, excelFile):
    global Threshold, CurveType, ExcelFile
    Threshold = threshold
    CurveType = curveType
    ExcelFile = excelFile

    getDeclineExcel()


def getDeclineExcel():
    global df, ProdType, ExcelFile

    df = pd.read_excel(ExcelFile)

    df = df.dropna(axis=1)
    if "Unnamed" in df.columns[0] and "Unnamed" in df.columns[1]:
        df.columns = df.iloc[0]
        df = df[1:]

    x_og = df.iloc[:, [0]]
    y_oil_og = df.iloc[:, [1]]
    y_gas_og = df.iloc[:, [2]]

    X = x_og[df.columns[0]].tolist()
    Y_oil = y_oil_og[df.columns[1]].tolist()
    Y_gas = y_gas_og[df.columns[2]].tolist()

    X = np.array(X, dtype=np.float64)
    Y_oil = np.array(Y_oil, dtype=np.float64)
    Y_gas = np.array(Y_gas, dtype=np.float64)

    plotDeclineCurve(X, Y_oil, Y_gas)


def plotDeclineCurve(T, Q_oil, Q_gas):
    global ProdType, CurveType, ChartThreshold
    ChartThreshold = Threshold

    if CurveType == "hyperbolic":
        hyp_decline_oil = decline_curve("hyperbolic", Q_oil[0])
        popt_hyp_oil, pcov_hyp_oil = curve_fit(hyp_decline_oil, T, Q_oil, method="trf")
        hyp_decline_gas = decline_curve("hyperbolic", Q_gas[0])
        popt_hyp_gas, pcov_hyp_gas = curve_fit(hyp_decline_gas, T, Q_gas, method="trf")

        T_list = T.tolist()
        for i in range(len(T_list), len(T_list) + 12):
            T_list.append(T_list[i - 1] + 1)
        T_ext = np.array(T_list, dtype=np.float64)
        pred_hyp_oil = hyp_decline_oil(T_ext, popt_hyp_oil[0], popt_hyp_oil[1])
        pred_hyp_gas = hyp_decline_gas(T_ext, popt_hyp_gas[0], popt_hyp_gas[1])

    elif CurveType == "exponential":
        exp_decline_oil = decline_curve("exponential", Q_oil[0])
        popt_exp_oil, pcov_exp_oil = curve_fit(exp_decline_oil, T, Q_oil, method="trf")
        exp_decline_gas = decline_curve("exponential", Q_gas[0])
        popt_exp_gas, pcov_exp_gas = curve_fit(exp_decline_gas, T, Q_gas, method="trf")

        T_list = T.tolist()
        for i in range(len(T_list), len(T_list) + 12):
            T_list.append(T_list[i - 1] + 1)
        T_ext = np.array(T_list, dtype=np.float64)
        pred_exp_oil = exp_decline_oil(T_ext, popt_exp_oil[0])
        pred_exp_gas = exp_decline_gas(T_ext, popt_exp_gas[0])

    if CurveType == "hyperbolic":
        declinePercentageList(T, Q_oil, Q_gas, T_ext, pred_hyp_oil, pred_hyp_gas)
    elif CurveType == "exponential":
        declinePercentageList(T, Q_oil, Q_gas, T_ext, pred_exp_oil, pred_exp_gas)


def declinePercentageList(T, Q_oil, Q_gas, T_ext, Q_pred_oil, Q_pred_gas):
    global Threshold

    oil_sum = 0
    for i in Q_oil:
        oil_sum += i
    oil_mean = oil_sum / len(Q_oil)

    gas_sum = 0
    for i in Q_gas:
        gas_sum += i
    gas_mean = gas_sum / len(Q_gas)

    oil_denominator = 0
    for i in Q_oil:
        oil_denominator += (i - oil_mean) ** 2

    gas_denominator = 0
    for i in Q_gas:
        gas_denominator += (i - gas_mean) ** 2

    oil_std_dev = math.sqrt(oil_denominator / len(Q_oil))
    gas_std_dev = math.sqrt(gas_denominator / len(Q_gas))
    perc = Threshold
    z_val = getDeclineZ(perc)

    oil_lower_bound = []
    gas_lower_bound = []
    for i in Q_oil:
        oil_lower_bound.append(i - (oil_std_dev * z_val))
        gas_lower_bound.append(i - (gas_std_dev * z_val))

    declinePercentageLine(T, oil_lower_bound, gas_lower_bound, Q_pred_oil, Q_pred_gas)


def getDeclineZ(perc):
    val = float(perc) / 100

    df = pd.read_csv(os.path.join(settings.BASE_DIR, "ObjectA/static/main/preData/new_z_table.csv"))
    df = df.drop('z', 1)
    val_list = df.values.tolist()

    row = [-1.6, -1.5, -1.4, -1.3, -1.2, -1.1, -1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0,
           0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]

    for i in range(len(val_list)):
        for j in range(len(val_list[i])):
            if val_list[i][j] > val:
                if 0 < i <= 16:
                    z_val = row[i] - ((j - 1) / 100)
                else:
                    z_val = row[i] + ((j - 1) / 100)

                return z_val


def declinePercentageLine(T, Q_oil, Q_gas, Q_Pred_oil, Q_Pred_gas):
    global CurveType, Chart, Excel_input

    if CurveType == "hyperbolic":
        hyp_decline_oil = decline_curve("hyperbolic", Q_oil[0])
        popt_hyp_oil, pcov_hyp_oil = curve_fit(hyp_decline_oil, T, Q_oil, method="trf")
        hyp_decline_gas = decline_curve("hyperbolic", Q_gas[0])
        popt_hyp_gas, pcov_hyp_gas = curve_fit(hyp_decline_gas, T, Q_gas, method="trf")

        T_list = T.tolist()
        for i in range(len(T_list), len(T_list) + 12):
            T_list.append(T_list[i - 1] + 1)
        T_ext = np.array(T_list, dtype=np.float64)
        pred_hyp_oil = hyp_decline_oil(T_ext, popt_hyp_oil[0], popt_hyp_oil[1])
        pred_hyp_gas = hyp_decline_gas(T_ext, popt_hyp_gas[0], popt_hyp_gas[1])

    elif CurveType == "exponential":
        exp_decline_oil = decline_curve("exponential", Q_oil[0])
        popt_exp_oil, pcov_exp_oil = curve_fit(exp_decline_oil, T, Q_oil, method="trf")
        exp_decline_gas = decline_curve("exponential", Q_gas[0])
        popt_exp_gas, pcov_exp_gas = curve_fit(exp_decline_gas, T, Q_gas, method="trf")

        T_list = T.tolist()
        for i in range(len(T_list), len(T_list) + 12):
            T_list.append(T_list[i - 1] + 1)
        T_ext = np.array(T_list, dtype=np.float64)
        pred_exp_oil = exp_decline_oil(T_ext, popt_exp_oil[0])
        pred_exp_gas = exp_decline_gas(T_ext, popt_exp_gas[0])

    if CurveType == "hyperbolic":
        # Excel_input = [T_ext, Q_Pred_oil, Q_Pred_gas, pred_hyp_oil, pred_hyp_gas, Threshold]
        # print(Excel_input)
        Excel_input = [pred_hyp_oil, pred_hyp_gas]
    elif CurveType == "exponential":
        # Excel_input = [T_ext, Q_Pred_oil, Q_Pred_gas, pred_exp_oil, pred_exp_gas, Threshold]
        # print(Excel_input)
        Excel_input = [pred_exp_oil, pred_exp_gas]
    # print(Excel_input[0][36:])
    # print(Excel_input[1][36:])
    # print(Excel_input)


def getZNorm(perc):
    val = (perc / 100) / 2

    df = pd.read_csv(os.path.join(settings.BASE_DIR, "ObjectABC/static/main/preData/z_table.csv"))
    df = df.drop('z', 1)
    val_list = df.values.tolist()

    for i in range(len(val_list)):
        for j in range(len(val_list[i])):
            if val_list[i][j] > val:
                z_val = (i / 10) + ((j - 1) / 100)
                return -z_val


def create_table():
    global percentile, OilPricei
    oil_mid = [OilPrice] * 12
    oil_perc = [OilPrice]

    z_val = getZNorm(float(percentile))

    std_dev_oil_price = (float(OilPrice) * float(OilSD)) / 100

    for i in range(1, len(oil_mid)):
        oil_perc.append(float(OilPrice) + (std_dev_oil_price * z_val * (i ** 0.5)))
    oil_perc[0] = float(oil_perc[0])

    return oil_perc


def create_gas_table():
    global percentile, GasPrice, GasSD
    gas_mid = [float(GasPrice)] * 12
    gas_perc = [GasPrice]

    z_val = getZNorm(float(percentile))

    std_dev_gas_price = (float(GasPrice) * float(GasSD)) / 100

    for i in range(1, len(gas_mid)):
        gas_perc.append(float(GasPrice) + (std_dev_gas_price * z_val * (i ** 0.5)))
    gas_perc[0] = float(gas_perc[0])

    return gas_perc


def getZ(perc):
    if perc >= 50:
        val = (perc - 50) / 100
    else:
        val = (50 - perc) / 100

    df = pd.read_csv(os.path.join(settings.BASE_DIR, "ObjectB/static/main/preData/z_table.csv"))
    df = df.drop('z', 1)
    val_list = df.values.tolist()

    for i in range(len(val_list)):
        for j in range(len(val_list[i])):
            if val_list[i][j] > val:
                z_val = (i / 10) + (j / 100)
                return z_val


def create_excel():
    global Response, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20, col21, col22, col23, col24, col25, FixedCost, InProdCost, Product, BC_MMSCFG, GOR, Royalty, OilProdCost, GasProdCost, CostBelowPerc, IndProdSD

    col1, col2 = [], []
    if Product == 'oil':
        col1 = Excel_input[0][-12:]
        for i in range(12):
            col2.append((float(GOR) * col1[i]) / 100)
    else:
        col2 = Excel_input[1][-12:]
        for i in range(12):
            col1.append((float(BC_MMSCFG) * col2[i]) / 100)

    col7 = col7.values.tolist()
    col8 = col8.values.tolist()
    col9 = col9.values.tolist()
    col10 = col10.values.tolist()

    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Expense")

    cell_format_red = workbook.add_format()
    cell_format_red.set_font_color('#FF0000')
    cell_format_purple = workbook.add_format()
    cell_format_purple.set_font_color('#800080')
    cell_format_lorange = workbook.add_format()
    cell_format_lorange.set_font_color('#C97016')
    cell_format_dgreen = workbook.add_format()
    cell_format_dgreen.set_font_color('#466B00')
    cell_format_brown = workbook.add_format()
    cell_format_brown.set_font_color('#946828')
    cell_format_dred = workbook.add_format()
    cell_format_dred.set_font_color('#520901')
    cell_format_skyblue = workbook.add_format()
    cell_format_skyblue.set_font_color('#1A92ED')
    cell_format_dbrown = workbook.add_format()
    cell_format_dbrown.set_font_color('#493313')

    worksheet.write(0, 0, "Month")
    worksheet.write(0, 1, "Percentile BOPD")
    worksheet.write(0, 2, "Percentile MSCFPD")
    worksheet.write(0, 3, "Percentile bbls/mo")
    worksheet.write(0, 4, "Percentile MSCF/mo")
    worksheet.write(0, 5, "NET Percentile bbls/mo")
    worksheet.write(0, 6, "NET Percentile MSCF/mo")
    worksheet.write(0, 7, "Hedged bbls/mo")
    worksheet.write(0, 8, "Hedged Price $/BO")
    worksheet.write(0, 9, "Hedged MCF/mo")
    worksheet.write(0, 10, "Hedged $/MCF")
    worksheet.write(0, 11, "Percentile (unhedged) Oil Price")
    worksheet.write(0, 12, "Unhedged bbls/mo")
    worksheet.write(0, 13, "Hedged Oil $/mo")
    worksheet.write(0, 14, "Unhedged Oil $/mo")
    worksheet.write(0, 15, "NET Percentile (unhedged) Gas Price", cell_format_red)
    worksheet.write(0, 16, "NET Unhedged MSCF/mo", cell_format_purple)
    worksheet.write(0, 17, "Hedged Gas $/mo")
    worksheet.write(0, 18, "Unhedged Gas $/mo", cell_format_lorange)
    worksheet.write(0, 19, "Total Revenue $/mo", cell_format_dgreen)
    worksheet.write(0, 20, "Fixed Cost ($/mo)")
    worksheet.write(0, 21, "Variable Independent of Production ($/mo)", cell_format_brown)
    worksheet.write(0, 22, "Variable Based on Oil Production ($/mo)", cell_format_dred)
    worksheet.write(0, 23, "Variable Based on Gas Production ($/mo)", cell_format_skyblue)
    worksheet.write(0, 24, "Total Expense ($/mo)", cell_format_dbrown)
    worksheet.write(0, 25, "Gross Profit ($/mo)")

    col11 = create_table()
    col15 = create_gas_table()
    col20 = [FixedCost] * 12

    for i in range(12):
        col3.append(30.42 * col1[i])
        col4.append(30.42 * col2[i])

    for i in range(12):
        col5.append(col3[i] * (1 - float(Royalty)))
        col6.append(col4[i] * (1 - float(Royalty)))

        col12.append(col5[i] - col7[i])
        col16.append(col6[i] - col9[i])

        col13.append(col7[i][0] * col8[i][0])
        col17.append(col9[i][0] * col10[i][0])

    varIndProd = getZ(int(CostBelowPerc))
    varIndProd *= float(IndProdSD)
    varIndProd += float(InProdCost)
    for i in range(12):
        col21.append(varIndProd)
        col22.append(col3[i] * float(OilProdCost))
        col23.append(col4[i] * float(GasProdCost))

    for i in range(12):
        col14.append(col12[i] * col11[i])
        col18.append(col16[i] * col15[i])

        col24.append(float(col20[i]) + float(col21[i]) + float(col22[i]) + float(col23[i]))

    for i in range(12):
        col19.append(col13[i] + col14[i] + col17[i] + col18[i])

    for i in range(12):
        col25.append(col19[i] - col24[i])

    for i in range(12):
        worksheet.write(i+1, 0, i+1)
        worksheet.write(i+1, 1, col1[i])
        worksheet.write(i+1, 2, col2[i])
        worksheet.write(i+1, 3, col3[i])
        worksheet.write(i+1, 4, col4[i])
        worksheet.write(i+1, 5, col5[i])
        worksheet.write(i+1, 6, col6[i])
        worksheet.write(i+1, 7, col7[i][0])
        worksheet.write(i+1, 8, col8[i][0])
        worksheet.write(i+1, 9, col9[i][0])
        worksheet.write(i+1, 10, col10[i][0])
        worksheet.write(i+1, 11, col11[i])
        worksheet.write(i+1, 12, col12[i])
        worksheet.write(i+1, 13, col13[i])
        worksheet.write(i+1, 14, col14[i])
        worksheet.write(i+1, 15, col15[i], cell_format_red)
        worksheet.write(i+1, 16, col16[i], cell_format_purple)
        worksheet.write(i+1, 17, col17[i])
        worksheet.write(i+1, 18, col18[i], cell_format_lorange)
        worksheet.write(i+1, 19, col19[i], cell_format_dgreen)
        worksheet.write(i+1, 20, col20[i])
        worksheet.write(i+1, 21, col21[i], cell_format_brown)
        worksheet.write(i+1, 22, col22[i], cell_format_dred)
        worksheet.write(i+1, 23, col23[i], cell_format_skyblue)
        worksheet.write(i+1, 24, col24[i], cell_format_dbrown)
        worksheet.write(i+1, 25, col25[i])

    workbook.close()

    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=Expense_Output.xlsx"
    output.close()
    Response = response

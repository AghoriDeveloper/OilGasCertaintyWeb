import io
import pandas as pd
import numpy as np
from django.http import HttpResponse
from scipy.optimize import curve_fit
import math
import xlsxwriter
import os
from django.conf import settings

Threshold, CurveType, ExcelFile, FixedCost, InProdCost, OilProdCost, GasProdCost, CostBelowPerc, IndProdSD = 0, 0, 0, 0, 0, 0, 0, 0, 0
Chart = -1
Response = -1
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = [], [], [], [], [], [], [], [], [], []
col11, col12, col13, col14, col15, col16, col17, col18, col19, col20 = [], [], [], [], [], [], [], [], [], []
col21, col22, col23, col24, col25 = [], [], [], [], []
percentile = 60.0
Excel_input = None

def setObjecCValues(threshold, curveType, excelFile, fixedCost, indProdCost, oilProdCost, gasProdCost, costBelowPerc, indProdSD):
    global Threshold, CurveType, ExcelFile, FixedCost, InProdCost, OilProdCost, GasProdCost, CostBelowPerc, IndProdSD
    Threshold = threshold
    CurveType = curveType
    ExcelFile = excelFile
    FixedCost = fixedCost
    InProdCost = indProdCost
    OilProdCost = oilProdCost
    GasProdCost = gasProdCost
    CostBelowPerc = costBelowPerc
    IndProdSD = indProdSD
    
    # getExcel()
    getDeclineCurveData(threshold, curveType, excelFile)
    create_excel()

    return Response


def getExcel():
    global df, Prod_perc, percentile, col7, col8, col9, col10, OutputExcelFile, HedgedExcelFile

    import_file_path = OutputExcelFile
    df = pd.read_excel(import_file_path)
    import_file_path = HedgedExcelFile
    df_hedged = pd.read_excel(import_file_path)

    col7 = df_hedged.iloc[:, [0]]
    col8 = df_hedged.iloc[:, [1]]
    col9 = df_hedged.iloc[:, [2]]
    col10 = df_hedged.iloc[:, [3]]

    percentile = Prod_perc
    df = df[1:]
    print(df)

    x_og = df.iloc[:, [0]]
    y_oil_og = df.iloc[:, [1]]
    y_gas_og = df.iloc[:, [2]]

    X = x_og[df.columns[0]].tolist()
    Y_oil = y_oil_og[df.columns[1]].tolist()
    Y_gas = y_gas_og[df.columns[2]].tolist()

    X = np.array(X, dtype=np.float64)
    Y_oil = np.array(Y_oil, dtype=np.float64)
    Y_gas = np.array(Y_gas, dtype=np.float64)

    plotCurve(X, Y_oil, Y_gas)


def decline_curve(curve_type, q_i):
    if curve_type == "exponential":
        def exponential_decline(T, a):
            return q_i * np.exp(-a * T)

        return exponential_decline

    elif curve_type == "hyperbolic":
        def hyperbolic_decline(T, a_i, b):
            return q_i / np.power((1 + b * a_i * T), 1. / b)

        return hyperbolic_decline


def L2_norm(Q, Q_obs):
    return np.sum(np.power(np.subtract(Q, Q_obs), 2))


def plotCurve(T, Q_oil, Q_gas):
    hyp_decline_oil = decline_curve("hyperbolic", Q_oil[0])
    hyp_decline_gas = decline_curve("hyperbolic", Q_gas[0])
    popt_hyp_oil, pcov_hyp_oil = curve_fit(hyp_decline_oil, T, Q_oil, method="trf")
    popt_hyp_gas, pcov_hyp_gas = curve_fit(hyp_decline_gas, T, Q_gas, method="trf")

    T_list = T.tolist()
    for i in range(len(T_list), len(T_list) + 12):
        T_list.append(T_list[i - 1] + 1)
    T_ext = np.array(T_list, dtype=np.float64)
    pred_hyp_oil = hyp_decline_oil(T_ext, popt_hyp_oil[0], popt_hyp_oil[1])
    pred_hyp_gas = hyp_decline_gas(T_ext, popt_hyp_gas[0], popt_hyp_gas[1])

    percentageList(T, Q_oil, Q_gas, T_ext, pred_hyp_oil, pred_hyp_gas)


def getZ(perc):
    val = perc / 100

    df = pd.read_csv(os.path.join(settings.BASE_DIR, "ObjectABC/static/main/preData/new_z_table.csv"))
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


def percentageList(T, Q_oil, Q_gas, T_ext, Q_pred_oil, Q_pred_gas):
    global percentile

    sum_oil = 0
    sum_gas = 0
    for i in range(len(Q_oil)):
        sum_oil += Q_oil[i]
        sum_gas += Q_gas[i]

    mean_oil = sum_oil / len(Q_oil)
    mean_gas = sum_gas / len(Q_gas)

    denominator_oil = 0
    denominator_gas = 0
    for i in range(len(Q_oil)):
        denominator_oil += (Q_oil[i] - mean_oil) ** 2
        denominator_gas += (Q_gas[i] - mean_gas) ** 2

    std_dev_oil = math.sqrt(denominator_oil / len(Q_oil))
    std_dev_gas = math.sqrt(denominator_gas / len(Q_gas))
    perc = int(percentile)

    z_val = getZ(perc)
    lower_bound_oil = []
    lower_bound_gas = []
    for i in range(len(Q_oil)):
        lower_bound_oil.append(Q_oil[i] - (std_dev_oil * z_val))
        lower_bound_gas.append(Q_gas[i] - (std_dev_gas * z_val))

    percentageLine(T, lower_bound_oil, lower_bound_gas, Q_pred_oil, Q_pred_gas)


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


# def create_table():
#     global percentile, OilPricei
#     oil_mid = [OilPrice] * 12
#     oil_perc = [OilPrice]
#
#     z_val = getZNorm(float(percentile))
#
#     std_dev_oil_price = (float(OilPrice) * float(OilSD)) / 100
#
#     for i in range(1, len(oil_mid)):
#         oil_perc.append(float(OilPrice) + (std_dev_oil_price * z_val * (i ** 0.5)))
#     oil_perc[0] = float(oil_perc[0])
#
#     return oil_perc


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


def create_excel():
    global Response, FixedCost, InProdCost, OilProdCost, GasProdCost, CostBelowPerc, IndProdSD, Excel_input

    col1 = Excel_input[0][36:]
    col3 = Excel_input[1][36:]
    col5 = [float(FixedCost)] * 12
    col8 = [float(InProdCost)] * 12

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
    worksheet.write(0, 1, "Oil Production BOPD")
    worksheet.write(0, 2, "Oil Production bbls/mo")
    worksheet.write(0, 3, "Gas Production MSCFPD")
    worksheet.write(0, 4, "Gas Production MSCF/mo")
    worksheet.write(0, 5, "Fixed Cost ($/mo)")
    worksheet.write(0, 6, "Variable Independent of Production ($/mo)", cell_format_brown)
    worksheet.write(0, 7, "Variable Based on Oil Production ($/mo)", cell_format_dred)
    worksheet.write(0, 8, "Variable Based on Gas Production ($/mo)", cell_format_skyblue)
    worksheet.write(0, 9, "Total Expense ($/mo)", cell_format_dbrown)

    col2, col4, col6, col7, col9 = [], [], [], [], []
    for i in range(12):
        col2.append(col1[i] + 30.4)
        col4.append(col3[i] + 30.4)

    for i in range(12):
        col6.append(col2[i] * float(OilProdCost))
        col7.append(col4[i] * float(GasProdCost))

    for i in range(12):
        col9.append(col5[i] + col6[i] + col7[i] + col8[i])

    for i in range(12):
        worksheet.write(i+1, 0, i+1)
        worksheet.write(i+1, 1, col1[i])
        worksheet.write(i+1, 2, col2[i])
        worksheet.write(i+1, 3, col3[i])
        worksheet.write(i+1, 4, col4[i])
        worksheet.write(i+1, 5, col5[i])
        worksheet.write(i+1, 6, col6[i])
        worksheet.write(i+1, 7, col7[i])
        worksheet.write(i+1, 8, col8[i])
        worksheet.write(i+1, 9, col9[i])

    workbook.close()

    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=Expense_Output.xlsx"
    output.close()
    Response = response


def percentageLine(T, Q_oil, Q_gas, Q_Pred_oil, Q_Pred_gas):
    hyp_decline_oil = decline_curve("hyperbolic", Q_oil[0])
    hyp_decline_gas = decline_curve("hyperbolic", Q_gas[0])
    popt_hyp_oil, pcov_hyp_oil = curve_fit(hyp_decline_oil, T, Q_oil, method="trf")
    popt_hyp_gas, pcov_hyp_gas = curve_fit(hyp_decline_gas, T, Q_gas, method="trf")

    T_list = T.tolist()
    for i in range(len(T_list), len(T_list) + 12):
        T_list.append(T_list[i - 1] + 1)
    T_ext = np.array(T_list, dtype=np.float64)
    pred_hyp_oil = hyp_decline_oil(T_ext, popt_hyp_oil[0], popt_hyp_oil[1])
    pred_hyp_gas = hyp_decline_gas(T_ext, popt_hyp_gas[0], popt_hyp_gas[1])

    create_excel(T_ext, Q_Pred_oil, Q_Pred_gas, pred_hyp_oil, pred_hyp_gas)


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
        Excel_input = [Q_Pred_oil, pred_hyp_oil]
    elif CurveType == "exponential":
        # Excel_input = [T_ext, Q_Pred_oil, Q_Pred_gas, pred_exp_oil, pred_exp_gas, Threshold]
        Excel_input = [Q_Pred_oil, pred_exp_oil]
    # print(Excel_input[0][36:])
    # print(Excel_input[1][36:])
    # print(Excel_input)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from scipy.optimize import curve_fit
import math
import xlsxwriter
from django.contrib.staticfiles.storage import staticfiles_storage
import os
from django.conf import settings
import base64
from io import BytesIO


ProdType, Threshold, CurveType, ExcelFile = '', 0, '', ''
Chart = -1

def setObjecAValues(prodType, threshold, curveType, excelFile):
    global ProdType, Threshold, CurveType, ExcelFile, Chart
    ProdType = prodType
    Threshold = threshold
    CurveType = curveType
    ExcelFile = excelFile
    
    getExcel()

    return Chart

def getExcel():
    global df, ProdType, ExcelFile

    df = pd.read_excel(ExcelFile)
    # print(ProdType)

    df = df.dropna(axis=1)
    if "Unnamed" in df.columns[0] and "Unnamed" in df.columns[1]:
        df.columns = df.iloc[0]
        df = df[1:]
    # print(df)

    if ProdType == "oil":
        x_og = df.iloc[:, [0]]
        y_og = df.iloc[:, [1]]

        X = x_og[df.columns[0]].tolist()
        Y = y_og[df.columns[1]].tolist()

    elif ProdType == "gas":
        x_og = df.iloc[:, [0]]
        y_og = df.iloc[:, [2]]

        X = x_og[df.columns[0]].tolist()
        Y = y_og[df.columns[2]].tolist()

    X = np.array(X, dtype=np.float64)
    Y = np.array(Y, dtype=np.float64)

    plotCurve(X, Y)


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


def plotCurve(T, Q):
    global ProdType, CurveType
    fig, ax = plt.subplots(1, figsize=(16, 16))
    ax.set_title("Decline Curve Analysis, " + str(Threshold) + "% Probability of Exceeding the Green Line", fontsize=18)
    ax.set_xlim(min(T) - 5, max(T) + 15)

    ax.scatter(T, Q, color="black", marker=".", s=250, linewidth=3)
    ax.set_xlabel("Time (Months)", fontsize=15)

    if ProdType == "oil":
        ax.set_ylabel("Production (BOPD)", fontsize=15)
    elif ProdType == "gas":
        ax.set_ylabel("Production (MSCFPD)", fontsize=15)

    if CurveType == "hyperbolic":
        hyp_decline = decline_curve("hyperbolic", Q[0])
        popt_hyp, pcov_hyp = curve_fit(hyp_decline, T, Q, method="trf")
        print(popt_hyp, pcov_hyp)
        # print("L2 Norm of hyperbolic decline decline: ", L2_norm(hyp_decline(T, popt_hyp[0], popt_hyp[1]), Q))

        T_list = T.tolist()
        for i in range(len(T_list), len(T_list) + 12):
            T_list.append(T_list[i - 1] + 1)
        T_ext = np.array(T_list, dtype=np.float64)
        pred_hyp = hyp_decline(T_ext, popt_hyp[0], popt_hyp[1])
        # print(Q)
        print(pred_hyp)

        min_val = min([min(curve) for curve in [pred_hyp]])
        max_val = max([max(curve) for curve in [pred_hyp]])

        ax.plot(T_ext, pred_hyp, color="green", linewidth=5, alpha=0.5, label="Hyperbolic Best Fit (" + str(Threshold) + "%)")
    elif CurveType == "exponential":
        exp_decline = decline_curve("exponential", Q[0])
        popt_exp, pcov_exp = curve_fit(exp_decline, T, Q, method="trf")
        # print("L2 Norm of exponential decline: ", L2_norm(exp_decline(T, popt_exp[0]), Q))

        T_list = T.tolist()
        for i in range(len(T_list), len(T_list) + 12):
            T_list.append(T_list[i - 1] + 1)
        T_ext = np.array(T_list, dtype=np.float64)
        pred_exp = exp_decline(T_ext, popt_exp[0])

        min_val = min([min(curve) for curve in [pred_exp]])
        max_val = max([max(curve) for curve in [pred_exp]])

        ax.plot(T_ext, pred_exp, color="green", linewidth=5, alpha=0.5, label="Exponential Best Fit (" + str(Threshold) + "%)")

    ax.set_ylim(min_val - 20, max_val + 20)
    # ax.ticklabel_format(fontsize=25)
    ax.legend(fontsize=15)
    # plt.show()

    if CurveType == "hyperbolic":
        percentageList(T, Q, T_ext, pred_hyp, ax)
    elif CurveType == "exponential":
        percentageList(T, Q, T_ext, pred_exp, ax)


def getZ(perc):
    val = int(perc) / 100

    df = pd.read_csv(os.path.join(settings.BASE_DIR, "ObjectA/static/main/preData/new_z_table.csv"))
    df = df.drop('z', 1)
    val_list = df.values.tolist()

    row = [-1.6, -1.5, -1.4, -1.3, -1.2, -1.1, -1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0,
           0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]

    for i in range(len(val_list)):
        for j in range(len(val_list[i])):
            if val_list[i][j] > val:
                # print(val)
                # print("Row:", i, ", Column:", j)

                if 0 < i <= 16:
                    z_val = row[i] - ((j - 1) / 100)
                else:
                    z_val = row[i] + ((j - 1) / 100)
                # print(z_val)
                return z_val


def percentageList(T, Q, T_ext, Q_pred, ax):
    global Threshold

    sum = 0
    for i in Q:
        sum += i
    mean = sum / len(Q)

    denominator = 0
    for i in Q:
        denominator += (i - mean) ** 2

    std_dev = math.sqrt(denominator / len(Q))

    perc = Threshold
    # print(perc)

    z_val = getZ(perc)

    # err_margin = (z_val * (std_dev / math.sqrt(len(Q))))

    lower_bound = []
    for i in Q:
        lower_bound.append(i - (std_dev * z_val))

    percentageLine(T, lower_bound, ax, Q_pred)


def create_excel(T_ext, Q_Pred, pred):
    workbook = xlsxwriter.Workbook(os.path.expanduser("~") + "/Downloads/" + 'Output.xlsx')
    worksheet = workbook.add_worksheet("Sheet")

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


def percentageLine(T, Q, ax, Q_Pred):
    global CurveType, Chart

    if CurveType == "hyperbolic":
        hyp_decline = decline_curve("hyperbolic", Q[0])
        popt_hyp, pcov_hyp = curve_fit(hyp_decline, T, Q, method="trf")
        # print("L2 Norm of hyperbolic decline decline: ", L2_norm(hyp_decline(T, popt_hyp[0], popt_hyp[1]), Q))

        T_list = T.tolist()
        for i in range(len(T_list), len(T_list) + 12):
            T_list.append(T_list[i - 1] + 1)
        T_ext = np.array(T_list, dtype=np.float64)
        pred_hyp = hyp_decline(T_ext, popt_hyp[0], popt_hyp[1])
        # print(Q)
        # print(pred_hyp)

        min_val = min([min(curve) for curve in [pred_hyp]])
        max_val = max([max(curve) for curve in [pred_hyp]])

        ax.plot(T_ext, pred_hyp, color="red", linewidth=5, alpha=0.5, label="Percentile Fit at " + str(Threshold) + "% Percentile")
    elif CurveType == "exponential":
        exp_decline = decline_curve("exponential", Q[0])
        popt_exp, pcov_exp = curve_fit(exp_decline, T, Q, method="trf")
        # print("L2 Norm of exponential decline: ", L2_norm(exp_decline(T, popt_exp[0]), Q))

        T_list = T.tolist()
        for i in range(len(T_list), len(T_list) + 12):
            T_list.append(T_list[i - 1] + 1)
        T_ext = np.array(T_list, dtype=np.float64)
        pred_exp = exp_decline(T_ext, popt_exp[0])

        min_val = min([min(curve) for curve in [pred_exp]])
        max_val = max([max(curve) for curve in [pred_exp]])

        ax.plot(T_ext, pred_exp, color="red", linewidth=5, alpha=0.5, label="Percentile Fit at " + str(Threshold) + "% Percentile")

    ax.set_ylim(min_val - 20, max_val + 20)
    # ax.ticklabel_format(fontsize=25)
    plt.legend(loc='upper right')
    ax.legend(fontsize=15)
    # plt.show()
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    if CurveType == "hyperbolic":
        create_excel(T_ext, Q_Pred, pred_hyp)
    elif CurveType == "exponential":
        create_excel(T_ext, Q_Pred, pred_exp)

    Chart = graph




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math
import xlsxwriter
from django.contrib.staticfiles.storage import staticfiles_storage
import os
from django.conf import settings
import base64
from io import BytesIO


OilPrice, OilSD, GasPrice, GasSD, PercLine = 0, 0, 0, 0, 0
Chart = -1

def setObjecBValues(oilPrice, oilSD, gasPrice, gasSD, percLine):
    global OilPrice, OilSD, GasPrice, GasSD, PercLine, Chart
    OilPrice = oilPrice
    OilSD = oilSD
    GasPrice = gasPrice
    GasSD = gasSD
    PercLine = percLine
    
    value_verify()

    return Chart


def getZ(perc):
    val = (perc / 100) / 2

    df = pd.read_csv(os.path.join(settings.BASE_DIR, "ObjectB/static/main/preData/z_table.csv"))
    df = df.drop('z', 1)
    val_list = df.values.tolist()

    for i in range(len(val_list)):
        for j in range(len(val_list[i])):
            if val_list[i][j] > val:
                # print(val)
                # print("Row:" , i, ", Column:", j)

                z_val = (i / 10) + ((j - 1) / 100)
                # print(z_val)
                return -z_val


def value_verify():
    global OilPrice, GasPrice

    oil_mid = [float(OilPrice)] * 12
    gas_mid = [float(GasPrice)] * 12

    create_table(oil_mid, gas_mid)
    # create_gas_table(gas_mid)


def create_table(oil_mid, gas_mid):
    global OilPrice, OilSD, GasPrice, GasSD, PercLine

    oil_perc = [OilPrice]
    gas_perc = [GasPrice]

    z_val = getZ(int(PercLine))

    std_dev_oil_price = (int(OilPrice) * int(OilSD)) / 100
    std_dev_gas_price = (int(GasPrice) * int(GasSD)) / 100

    for i in range(1, len(oil_mid)):
        # oil_perc.append((oil_mid[i] - z_val) * (i ** 0.5))
        oil_perc.append(float(OilPrice) + (std_dev_oil_price * z_val * (i ** 0.5)))
        gas_perc.append(float(GasPrice) + (std_dev_gas_price * z_val * (i ** 0.5)))
    oil_perc[0] = float(oil_perc[0])
    gas_perc[0] = float(gas_perc[0])
    print("Oil Ouput: " + str(oil_perc))
    print("Gas Ouput: " + str(gas_perc))

    bar_plot(oil_perc, gas_perc)


def bar_plot(oil_perc, gas_perc):
    global Chart

    fig, a = plt.subplots(1, 2, squeeze=False)
    label = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    oil_perc = [int(a) for a in oil_perc]

    # plt.bar(label, oil_perc, color='orange', width=0.4)
    a[0][0].plot(label, oil_perc)
    a[0][0].plot(label, oil_perc, '*')

    plt.xlabel("Months")
    plt.ylim(min(oil_perc)-5, max(oil_perc)+5)
    plt.ylabel("Assumed Price and Percentile Price")
    a[0][0].set_title("Oil Percentile Price")

    a[0][1].plot(label, gas_perc)
    a[0][1].plot(label, gas_perc, '*')

    # a[0][1].xlabel("Months")
    # a[0][1].ylim(min(gas_perc) - 5, max(gas_perc) + 5)
    # a[0][1].ylabel("Assumed Price and Percentile Price")
    a[0][1].set_title("Gas Percentile Price")
    # plt.show()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    Chart = graph
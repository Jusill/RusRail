import os
import sys

import xlrd

import numpy as np
import pandas as pd

import Config
import Functions

sys._enablelegacywindowsfsencoding()

mode = int(input("Выбрете тип ввод данных \n > 1: Ввести диаметр разбиения \n > 2: Ввести количество отрезков "
                 "разбиения \n"))

if mode == 1:
    delta = float(input("Введите диаметр: "))
elif mode == 2:
    n = int(input("Введите количество отрезков: "))

global_list_1 = list()
global_list_2 = list()

for name in os.listdir("data/input"):

    ii = 0

    while True:

        if name[-4:] == "xlsx" or name[-3:] == "xls":
            try:
                excel_file = pd.ExcelFile("data/input/" + name)
                print(excel_file.sheet_names[ii])
                df = pd.read_excel(excel_file, sheet_name=excel_file.sheet_names[ii])
                l = list()
                k = pd.DataFrame()

                for i in list(df[df.columns[0]].axes[0]):
                    if i == 'Ось № ' or i == 'Коэффициент':
                        continue
                    if i == 'Среднее':
                        break

                    l.append(i)

                k['№ Оси'] = l
                l.clear()

                for j in range(8):
                    for i in list(df[df.columns[0]].axes[0]):
                        if i == 'Ось № ' or i == 'Коэффициент':
                            continue
                        if i == 'Среднее':
                            break

                        if type(df[df.columns[j]][i]) is pd.core.series.Series:
                            l.append(df[df.columns[j]][i].values[0])
                        else:
                            l.append(df[df.columns[j]][i])

                    k['Force_' + str(j)] = l
                    l.clear()
                df = k.copy()
            except FileNotFoundError:
                continue

        elif name[-3:] == "csv":
            try:
                df = pd.read_csv("data/input/" + name, encoding="windows-1251", sep=";")
            except FileNotFoundError:
                continue
        else:
            continue

        if name[-4:] == "xlsx":
            name_f = name[:-5] + " " + excel_file.sheet_names[ii]
        elif name[-3:] == "xls" or name[-3:] == "csv":
            name_f = name[:-4]

        if mode == 1:
            vals_d_1 = list()
            vals_d_2 = list()

            for i in df.index:
                vals_d_1.append([float(str(df[df.columns[0]][i]).replace(',', '.')),
                                 float(str(df[df.columns[1]][i]).replace(',', '.')),
                                 float(str(df[df.columns[2]][i]).replace(',', '.')),
                                 float(str(df[df.columns[3]][i]).replace(',', '.')),
                                 float(str(df[df.columns[4]][i]).replace(',', '.'))])

                vals_d_2.append([float(str(df[df.columns[0]][i]).replace(',', '.')),
                                 float(str(df[df.columns[5]][i]).replace(',', '.')),
                                 float(str(df[df.columns[6]][i]).replace(',', '.')),
                                 float(str(df[df.columns[7]][i]).replace(',', '.')),
                                 float(str(df[df.columns[8]][i]).replace(',', '.'))])
            df.drop(df.index, inplace=True)

            m1 = np.array(vals_d_1).astype(np.float)
            m2 = np.array(vals_d_2).astype(np.float)

            global_list_1.extend(vals_d_1)
            global_list_2.extend(vals_d_2)

            vals_d_1.clear()
            vals_d_2.clear()

            try:
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "1", exist_ok=True)
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "2", exist_ok=True)
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "3", exist_ok=True)
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "4", exist_ok=True)
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "1+3", exist_ok=True)
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "2+4", exist_ok=True)
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "all", exist_ok=True)

                for i in range(4):

                    axis = str(i + 1)
                    k = 1

                    for j in range(1, 5):
                        Functions.save_to_png(m1, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + axis + Config.d[k], i)
                        Functions.save_to_png(m2, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + axis + Config.d[k + 1], i)

                        Functions.save_to_cvs(m1, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + axis + Config.d[k], i)
                        Functions.save_to_cvs(m2, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + axis + Config.d[k + 1], i)
                        k = k + 2

                k = 1
                for j in range(1, 5):
                    Functions.save_to_png(m1, j, delta, "data/output/" + name_f + "_сделано"
                                          + "/" + "all" + Config.d[k])
                    Functions.save_to_png(m2, j, delta, "data/output/" + name_f + "_сделано"
                                          + "/" + "all" + Config.d[k + 1])

                    Functions.save_to_cvs(m1, j, delta, "data/output/" + name_f + "_сделано"
                                          + "/" + "all" + Config.d[k])
                    Functions.save_to_cvs(m2, j, delta, "data/output/" + name_f + "_сделано"
                                          + "/" + "all" + Config.d[k + 1])
                    k = k + 2

                for i in range(2):

                    if i == 0:
                        str_n = "1+3"
                    else:
                        str_n = "2+4"

                    k = 1
                    for j in range(1, 5):
                        Functions.save_to_png(m1, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + str_n + Config.d[k], i, 1)
                        Functions.save_to_png(m2, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + str_n + Config.d[k + 1], i, 1)

                        Functions.save_to_cvs(m1, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + str_n + Config.d[k], i, 1)
                        Functions.save_to_cvs(m2, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + str_n + Config.d[k + 1], i, 1)
                        k = k + 2

            except FileExistsError or OSError:
                for i in range(4):

                    axis = str(i + 1)
                    k = 1

                    for j in range(1, 5):
                        Functions.save_to_png(m1, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + axis + Config.d[k], i)
                        Functions.save_to_png(m2, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + axis + Config.d[k + 1], i)

                        Functions.save_to_cvs(m1, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + axis + Config.d[k], i)
                        Functions.save_to_cvs(m2, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + axis + Config.d[k + 1], i)

                        k = k + 2

                k = 1
                for j in range(1, 5):
                    Functions.save_to_png(m1, j, delta, "data/output/" + name_f + "_сделано"
                                          + "/" + "all" + Config.d[k])
                    Functions.save_to_png(m2, j, delta, "data/output/" + name_f + "_сделано"
                                          + "/" + "all" + Config.d[k + 1])

                    Functions.save_to_cvs(m1, j, delta, "data/output/" + name_f + "_сделано"
                                          + "/" + "all" + Config.d[k])
                    Functions.save_to_cvs(m2, j, delta, "data/output/" + name_f + "_сделано"
                                          + "/" + "all" + Config.d[k + 1])
                    k = k + 2

                for i in range(2):
                    k = 1

                    if i == 0:
                        str_n = "1+3"
                    else:
                        str_n = "2+4"

                    for j in range(1, 5):
                        Functions.save_to_png(m1, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + str_n + Config.d[k], i, 1)
                        Functions.save_to_png(m2, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + str_n + Config.d[k + 1], i, 1)

                        Functions.save_to_cvs(m1, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + str_n + Config.d[k], i, 1)
                        Functions.save_to_cvs(m2, j, delta, "data/output/" + name_f + "_сделано"
                                              + "/" + str_n + Config.d[k + 1], i, 1)
                        k = k + 2

        elif mode == 2:
            vals_d_1 = list()
            vals_d_2 = list()

            for i in df.index:
                vals_d_1.append([float(str(df[df.columns[0]][i]).replace(',', '.')),
                                 float(str(df[df.columns[1]][i]).replace(',', '.')),
                                 float(str(df[df.columns[2]][i]).replace(',', '.')),
                                 float(str(df[df.columns[3]][i]).replace(',', '.')),
                                 float(str(df[df.columns[4]][i]).replace(',', '.'))])

                vals_d_2.append([float(str(df[df.columns[0]][i]).replace(',', '.')),
                                 float(str(df[df.columns[5]][i]).replace(',', '.')),
                                 float(str(df[df.columns[6]][i]).replace(',', '.')),
                                 float(str(df[df.columns[7]][i]).replace(',', '.')),
                                 float(str(df[df.columns[8]][i]).replace(',', '.'))])

            m1 = np.array(vals_d_1).astype(np.float)
            m2 = np.array(vals_d_2).astype(np.float)

            global_list_1.extend(vals_d_1)
            global_list_2.extend(vals_d_2)

            vals_d_1.clear()
            vals_d_2.clear()

            try:
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "1", exist_ok=True)
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "2", exist_ok=True)
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "3", exist_ok=True)
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "4", exist_ok=True)
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "1+3", exist_ok=True)
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "2+4", exist_ok=True)
                os.makedirs("data/output/" + name_f + "_сделано" + "/" + "all", exist_ok=True)

                for i in range(4):
                    axis = str(i + 1)
                    k = 1

                    for j in range(1, 5):
                        Functions.save_to_png_n(m1, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + axis + Config.d[k], i)
                        Functions.save_to_png_n(m2, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + axis + Config.d[k + 1], i)

                        Functions.save_to_cvs_n(m1, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + axis + Config.d[k], i)
                        Functions.save_to_cvs_n(m2, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + axis + Config.d[k + 1], i)
                        k = k + 2

                k = 1
                for j in range(1, 5):
                    Functions.save_to_png_n(m1, j, n, "data/output/" + name_f + "_сделано"
                                            + "/" + "all" + Config.d[k])
                    Functions.save_to_png_n(m2, j, n, "data/output/" + name_f + "_сделано"
                                            + "/" + "all" + Config.d[k + 1])

                    Functions.save_to_cvs_n(m1, j, n, "data/output/" + name_f + "_сделано"
                                            + "/" + "all" + Config.d[k])
                    Functions.save_to_cvs_n(m2, j, n, "data/output/" + name_f + "_сделано"
                                            + "/" + "all" + Config.d[k + 1])
                    k = k + 2

                for i in range(2):

                    if i == 0:
                        str_n = "1+3"
                    else:
                        str_n = "2+4"

                    k = 1
                    for j in range(1, 5):
                        Functions.save_to_png_n(m1, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + str_n + Config.d[k], i, 1)
                        Functions.save_to_png_n(m2, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + str_n + Config.d[k + 1], i, 1)

                        Functions.save_to_cvs_n(m1, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + str_n + Config.d[k], i, 1)
                        Functions.save_to_cvs_n(m2, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + str_n + Config.d[k + 1], i, 1)
                        k = k + 2

            except FileExistsError or OSError:
                for i in range(4):

                    axis = str(i + 1)
                    k = 1

                    for j in range(1, 5):
                        Functions.save_to_png_n(m1, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + axis + Config.d[k], i)
                        Functions.save_to_png_n(m2, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + axis + Config.d[k + 1], i)

                        Functions.save_to_cvs_n(m1, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + axis + Config.d[k], i)
                        Functions.save_to_cvs_n(m2, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + axis + Config.d[k + 1], i)
                        k = k + 2

                k = 1
                for j in range(1, 5):
                    Functions.save_to_png_n(m1, j, n, "data/output/" + name_f + "_сделано"
                                            + "/" + "all" + Config.d[k])
                    Functions.save_to_png_n(m2, j, n, "data/output/" + name_f + "_сделано"
                                            + "/" + "all" + Config.d[k + 1])

                    Functions.save_to_cvs_n(m1, j, n, "data/output/" + name_f + "_сделано"
                                            + "/" + "all" + Config.d[k])
                    Functions.save_to_cvs_n(m2, j, n, "data/output/" + name_f + "_сделано"
                                            + "/" + "all" + Config.d[k + 1])
                    k = k + 2

                for i in range(2):

                    if i == 0:
                        str_n = "1+3"
                    else:
                        str_n = "2+4"

                    k = 1
                    for j in range(1, 5):
                        Functions.save_to_png_n(m1, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + str_n + Config.d[k], i, 1)
                        Functions.save_to_png_n(m2, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + str_n + Config.d[k + 1], i, 1)

                        Functions.save_to_cvs_n(m1, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + str_n + Config.d[k], i, 1)
                        Functions.save_to_cvs_n(m2, j, n, "data/output/" + name_f + "_сделано"
                                                + "/" + str_n + Config.d[k + 1], i, 1)
                        k = k + 2

        ii = ii + 1
        try:
            if excel_file.sheet_names[ii] == 'Лист1':
                ii = 0
                break
        except IndexError:
            ii = 0
            break

    print(name + " успешно обработан!")


if mode == 1:
    m1 = np.array(global_list_1).astype(np.float)
    m2 = np.array(global_list_2).astype(np.float)

    global_list_1.clear()
    global_list_2.clear()

    try:
        os.makedirs("data/output/Global_сделано" + "/" + "1", exist_ok=True)
        os.makedirs("data/output/Global_сделано" + "/" + "2", exist_ok=True)
        os.makedirs("data/output/Global_сделано" + "/" + "3", exist_ok=True)
        os.makedirs("data/output/Global_сделано" + "/" + "4", exist_ok=True)
        os.makedirs("data/output/Global_сделано" + "/" + "1+3", exist_ok=True)
        os.makedirs("data/output/Global_сделано" + "/" + "2+4", exist_ok=True)
        os.makedirs("data/output/Global_сделано" + "/" + "all", exist_ok=True)

        for i in range(4):

            axis = str(i + 1)
            k = 1

            for j in range(1, 5):
                Functions.save_to_png(m1, j, delta, "data/output/Global_сделано"
                                      + "/" + axis + Config.d[k], i)
                Functions.save_to_png(m2, j, delta, "data/output/Global_сделано"
                                      + "/" + axis + Config.d[k + 1], i)

                Functions.save_to_cvs(m1, j, delta, "data/output/Global_сделано"
                                      + "/" + axis + Config.d[k], i)
                Functions.save_to_cvs(m2, j, delta, "data/output/Global_сделано"
                                      + "/" + axis + Config.d[k + 1], i)
                k = k + 2

        k = 1
        for j in range(1, 5):
            Functions.save_to_png(m1, j, delta, "data/output/Global_сделано"
                                  + "/" + "all" + Config.d[k])
            Functions.save_to_png(m2, j, delta, "data/output/Global_сделано"
                                  + "/" + "all" + Config.d[k + 1])

            Functions.save_to_cvs(m1, j, delta, "data/output/Global_сделано"
                                  + "/" + "all" + Config.d[k])
            Functions.save_to_cvs(m2, j, delta, "data/output/Global_сделано"
                                  + "/" + "all" + Config.d[k + 1])
            k = k + 2

        for i in range(2):

            if i == 0:
                str_n = "1+3"
            else:
                str_n = "2+4"

            k = 1
            for j in range(1, 5):
                Functions.save_to_png(m1, j, delta, "data/output/Global_сделано"
                                      + "/" + str_n + Config.d[k], i, 1)
                Functions.save_to_png(m2, j, delta, "data/output/Global_сделано"
                                      + "/" + str_n + Config.d[k + 1], i, 1)

                Functions.save_to_cvs(m1, j, delta, "data/output/Global_сделано"
                                      + "/" + str_n + Config.d[k], i, 1)
                Functions.save_to_cvs(m2, j, delta, "data/output/Global_сделано"
                                      + "/" + str_n + Config.d[k + 1], i, 1)
                k = k + 2

    except FileExistsError or OSError:
        for i in range(4):

            axis = str(i + 1)
            k = 1

            for j in range(1, 5):
                Functions.save_to_png(m1, j, delta, "data/output/Global_сделано"
                                      + "/" + axis + Config.d[k], i)
                Functions.save_to_png(m2, j, delta, "data/output/Global_сделано"
                                      + "/" + axis + Config.d[k + 1], i)

                Functions.save_to_cvs(m1, j, delta, "data/output/Global_сделано"
                                      + "/" + axis + Config.d[k], i)
                Functions.save_to_cvs(m2, j, delta, "data/output/Global_сделано"
                                      + "/" + axis + Config.d[k + 1], i)

                k = k + 2

        k = 1
        for j in range(1, 5):
            Functions.save_to_png(m1, j, delta, "data/output/Global_сделано"
                                  + "/" + "all" + Config.d[k])
            Functions.save_to_png(m2, j, delta, "data/output/Global_сделано"
                                  + "/" + "all" + Config.d[k + 1])

            Functions.save_to_cvs(m1, j, delta, "data/output/Global_сделано"
                                  + "/" + "all" + Config.d[k])
            Functions.save_to_cvs(m2, j, delta, "data/output/Global_сделано"
                                  + "/" + "all" + Config.d[k + 1])
            k = k + 2

        for i in range(2):
            k = 1

            if i == 0:
                str_n = "1+3"
            else:
                str_n = "2+4"

            for j in range(1, 5):
                Functions.save_to_png(m1, j, delta, "data/output/Global_сделано"
                                      + "/" + str_n + Config.d[k], i, 1)
                Functions.save_to_png(m2, j, delta, "data/output/Global_сделано"
                                      + "/" + str_n + Config.d[k + 1], i, 1)

                Functions.save_to_cvs(m1, j, delta, "data/output/Global_сделано"
                                      + "/" + str_n + Config.d[k], i, 1)
                Functions.save_to_cvs(m2, j, delta, "data/output/Global_сделано"
                                      + "/" + str_n + Config.d[k + 1], i, 1)
                k = k + 2

elif mode == 2:
    m1 = np.array(global_list_1).astype(np.float)
    m2 = np.array(global_list_2).astype(np.float)

    global_list_1.clear()
    global_list_2.clear()

    try:
        os.makedirs("data/output/Global_сделано/1", exist_ok=True)
        os.makedirs("data/output/Global_сделано/2", exist_ok=True)
        os.makedirs("data/output/Global_сделано/3", exist_ok=True)
        os.makedirs("data/output/Global_сделано/4", exist_ok=True)
        os.makedirs("data/output/Global_сделано/1+3", exist_ok=True)
        os.makedirs("data/output/Global_сделано/2+4", exist_ok=True)
        os.makedirs("data/output/Global_сделано/all", exist_ok=True)

        for i in range(4):
            axis = str(i + 1)
            k = 1

            for j in range(1, 5):
                Functions.save_to_png_n(m1, j, n, "data/output/Global_сделано"
                                        + "/" + axis + Config.d[k], i)
                Functions.save_to_png_n(m2, j, n, "data/output/Global_сделано"
                                        + "/" + axis + Config.d[k + 1], i)

                Functions.save_to_cvs_n(m1, j, n, "data/output/Global_сделано"
                                        + "/" + axis + Config.d[k], i)
                Functions.save_to_cvs_n(m2, j, n, "data/output/Global_сделано"
                                        + "/" + axis + Config.d[k + 1], i)
                k = k + 2

        k = 1
        for j in range(1, 5):
            Functions.save_to_png_n(m1, j, n, "data/output/Global_сделано"
                                    + "/" + "all" + Config.d[k])
            Functions.save_to_png_n(m2, j, n, "data/output/Global_сделано"
                                    + "/" + "all" + Config.d[k + 1])

            Functions.save_to_cvs_n(m1, j, n, "data/output/Global_сделано"
                                    + "/" + "all" + Config.d[k])
            Functions.save_to_cvs_n(m2, j, n, "data/output/Global_сделано"
                                    + "/" + "all" + Config.d[k + 1])
            k = k + 2

        for i in range(2):

            if i == 0:
                str_n = "1+3"
            else:
                str_n = "2+4"

            k = 1
            for j in range(1, 5):
                Functions.save_to_png_n(m1, j, n, "data/output/Global_сделано"
                                        + "/" + str_n + Config.d[k], i, 1)
                Functions.save_to_png_n(m2, j, n, "data/output/Global_сделано"
                                        + "/" + str_n + Config.d[k + 1], i, 1)

                Functions.save_to_cvs_n(m1, j, n, "data/output/Global_сделано"
                                        + "/" + str_n + Config.d[k], i, 1)
                Functions.save_to_cvs_n(m2, j, n, "data/output/Global_сделано"
                                        + "/" + str_n + Config.d[k + 1], i, 1)
                k = k + 2

    except FileExistsError or OSError:
        for i in range(4):

            axis = str(i + 1)
            k = 1

            for j in range(1, 5):
                Functions.save_to_png_n(m1, j, n, "data/output/Global_сделано"
                                        + "/" + axis + Config.d[k], i)
                Functions.save_to_png_n(m2, j, n, "data/output/Global_сделано"
                                        + "/" + axis + Config.d[k + 1], i)

                Functions.save_to_cvs_n(m1, j, n, "data/output/Global_сделано"
                                        + "/" + axis + Config.d[k], i)
                Functions.save_to_cvs_n(m2, j, n, "data/output/Global_сделано"
                                        + "/" + axis + Config.d[k + 1], i)
                k = k + 2

        k = 1
        for j in range(1, 5):
            Functions.save_to_png_n(m1, j, n, "data/output/Global_сделано"
                                    + "/" + "all" + Config.d[k])
            Functions.save_to_png_n(m2, j, n, "data/output/Global_сделано"
                                    + "/" + "all" + Config.d[k + 1])

            Functions.save_to_cvs_n(m1, j, n, "data/output/Global_сделано"
                                    + "/" + "all" + Config.d[k])
            Functions.save_to_cvs_n(m2, j, n, "data/output/Global_сделано"
                                    + "/" + "all" + Config.d[k + 1])
            k = k + 2

        for i in range(2):

            if i == 0:
                str_n = "1+3"
            else:
                str_n = "2+4"

            k = 1
            for j in range(1, 5):
                Functions.save_to_png_n(m1, j, n, "data/output/Global_сделано"
                                        + "/" + str_n + Config.d[k], i, 1)
                Functions.save_to_png_n(m2, j, n, "data/output/Global_сделано"
                                        + "/" + str_n + Config.d[k + 1], i, 1)

                Functions.save_to_cvs_n(m1, j, n, "data/output/Global_сделано"
                                        + "/" + str_n + Config.d[k], i, 1)
                Functions.save_to_cvs_n(m2, j, n, "data/output/Global_сделано"
                                        + "/" + str_n + Config.d[k + 1], i, 1)
                k = k + 2

print("Global успешно создан!")
input("Нажмите Enter... ")

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def calc_n(m, num_force, delta, num_axis=-1, mode=-1):
    if num_axis != -1 and mode == -1:
        return int((m[num_axis::4, num_force].max() - m[num_axis::4, num_force].min()) / delta)
    elif num_axis != -1 and mode == 1:
        return int((m[num_axis::2, num_force].max() - m[num_axis::2, num_force].min()) / delta)
    else:
        return int((m[::1, num_force].max() - m[::1, num_force].min()) / delta)


def save_to_png(m, num_force, delta, filename, num_axis=-1, mode=-1):
    if num_axis != -1 and mode == -1:
        plt.hist(m[num_axis::4, num_force], calc_n(m, num_force, delta, num_axis))
        plt.savefig(filename + '.png')
        plt.clf()
    elif num_axis != -1 and mode == 1:
        plt.hist(m[num_axis::2, num_force], calc_n(m, num_force, delta, num_axis))
        plt.savefig(filename + '.png')
        plt.clf()
    else:
        plt.hist(m[::1, num_force], calc_n(m, num_force, delta))
        plt.savefig(filename + '.png')
        plt.clf()


def save_to_cvs(m, num_force, delta, filename, num_axis=-1, mode=-1):
    vals = list()

    if num_axis != -1 and mode == -1:
        pivot = m[num_axis::4, num_force].min()
        n = calc_n(m, num_force, delta, num_axis)
        delta_real = ((m[num_axis::4, num_force].max() - m[num_axis::4, num_force].min()) / n)
        n_m = m[num_axis::4, num_force]

        for j in range(n):
            mask = (pivot <= n_m) * (n_m < pivot + delta_real)
            vals.append([len(n_m[mask]), str(pivot) + " -- " + str(pivot + delta_real)])
            pivot = pivot + delta_real

        pd.DataFrame({'count': np.array(vals)[::1, 0], 'range': np.array(vals)[::1, 1]}) \
            .to_csv(filename + '.csv', sep=';', encoding='utf-8')

        vals.clear()
    elif num_axis != -1 and mode == 1:
        pivot = m[num_axis::2, num_force].min()
        n = calc_n(m, num_force, delta, num_axis)
        delta_real = ((m[num_axis::2, num_force].max() - m[num_axis::2, num_force].min()) / n)
        n_m = m[num_axis::2, num_force]

        for j in range(n):
            mask = (pivot <= n_m) * (n_m < pivot + delta_real)
            vals.append([len(n_m[mask]), str(pivot) + " -- " + str(pivot + delta_real)])
            pivot = pivot + delta_real

        pd.DataFrame({'count': np.array(vals)[::1, 0], 'range': np.array(vals)[::1, 1]}) \
            .to_csv(filename + '.csv', sep=';', encoding='utf-8')

        vals.clear()
    else:
        pivot = m[::1, num_force].min()
        n = calc_n(m, num_force, delta, num_axis)
        delta_real = ((m[::1, num_force].max() - m[::1, num_force].min()) / n)
        n_m = m[::1, num_force]

        for j in range(n):
            mask = (pivot <= n_m) * (n_m < pivot + delta_real)
            vals.append([len(n_m[mask]), str(pivot) + " -- " + str(pivot + delta_real)])
            pivot = pivot + delta_real

        pd.DataFrame({'count': np.array(vals)[::1, 0], 'range': np.array(vals)[::1, 1]}) \
            .to_csv(filename + '.csv', sep=';', encoding='utf-8')

        vals.clear()


def save_to_png_n(m, num_force, n, filename, num_axis=-1, mode=-1):
    if num_axis != -1 and mode == -1:
        plt.hist(m[num_axis::4, num_force], n)
        plt.savefig(filename + '.png')
        plt.clf()
    elif num_axis != -1 and mode == 1:
        plt.hist(m[num_axis::2, num_force], n)
        plt.savefig(filename + '.png')
        plt.clf()
    else:
        plt.hist(m[::1, num_force], n)
        plt.savefig(filename + '.png')
        plt.clf()


def save_to_cvs_n(m, num_force, n, filename, num_axis=-1, mode=-1):
    vals = list()

    if num_axis != -1 and mode == -1:
        pivot = m[num_axis::4, num_force].min()
        delta_real = ((m[num_axis::4, num_force].max() - m[num_axis::4, num_force].min()) / n)
        n_m = m[num_axis::4, num_force]

        for j in range(n):
            mask = (pivot <= n_m) * (n_m < pivot + delta_real)
            vals.append([len(n_m[mask]), str(pivot) + " -- " + str(pivot + delta_real)])
            pivot = pivot + delta_real

        pd.DataFrame({'count': np.array(vals)[::1, 0], 'range': np.array(vals)[::1, 1]}) \
            .to_csv(filename + '.csv', sep=';', encoding='utf-8')

        vals.clear()
    elif num_axis != -1 and mode == 1:
        pivot = m[num_axis::2, num_force].min()
        delta_real = ((m[num_axis::2, num_force].max() - m[num_axis::2, num_force].min()) / n)
        n_m = m[num_axis::2, num_force]

        for j in range(n):
            mask = (pivot <= n_m) * (n_m < pivot + delta_real)
            vals.append([len(n_m[mask]), str(pivot) + " -- " + str(pivot + delta_real)])
            pivot = pivot + delta_real

        pd.DataFrame({'count': np.array(vals)[::1, 0], 'range': np.array(vals)[::1, 1]}) \
            .to_csv(filename + '.csv', sep=';', encoding='utf-8')

        vals.clear()
    else:
        pivot = m[::1, num_force].min()
        delta_real = ((m[::1, num_force].max() - m[::1, num_force].min()) / n)
        n_m = m[::1, num_force]

        for j in range(n):
            mask = (pivot <= n_m) * (n_m < pivot + delta_real)
            vals.append([len(n_m[mask]), str(pivot) + " -- " + str(pivot + delta_real)])
            pivot = pivot + delta_real

        pd.DataFrame({'count': np.array(vals)[::1, 0], 'range': np.array(vals)[::1, 1]}) \
            .to_csv(filename + '.csv', sep=';', encoding='utf-8')

        vals.clear()

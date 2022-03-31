from cProfile import run
import csv
import numpy as np
import array
import ROOT as r


NAMES = [
    "phase",
    "dt_ch1", "vpp1_ch1", "vpp2_ch1",
    "dt_ch2", "vpp1_ch2", "vpp2_ch2",
    "dt_ch3", "vpp1_ch3", "vpp2_ch3",
    "dt_ch4", "vpp1_ch4", "vpp2_ch4"
]

R_BPM = 38/2 # [mm]

def read_csv(filename: str = '/Users/yuto/VS/acc_intern/data/by_tomoes_eye.csv'):
    with open(filename) as f:
        reader = csv.reader(f)
        ret = []
        for r in reader:
            if r[0][0] == '#': continue
            ret.append(list(map(float, r)))
    ret = np.array(ret)
    ret = {
        NAMES[i]: ret.T[i]
        for i in range(len(NAMES))
    }
    return ret

def calibration_function(x):
    sum_ch_voltage = 25.909 + 16.364 + 13.636 + 17.273
    charge = 1.8322e-9
    return x * (charge / sum_ch_voltage)

def read_wf_csv(filename: str = '/Users/yuto/VS/acc_intern/data/osc/e+_run01.csv'):
    with open(filename) as f:
        reader = csv.reader(f)
        ret = list(reader)
    ret = np.array(ret, dtype=float).T
    return ret

def calc_channel_sum_error_propagation(errors = (1, 2, 3, 4)):
    ret = 0
    for e in errors:
        ret += e**2
    ret = ret**(1/2)
    return ret

def TPGraph(n, x, y):
    x = array.array('d', x)
    y = array.array('d', y)
    return r.TGraph(n, x, y)

def TPGraphErrors(n, x, y, ex, ey):
    x = array.array('d', x)
    y = array.array('d', y)
    ex = array.array('d', ex)
    ey = array.array('d', ey)
    return r.TGraphErrors(n, x, y, ex, ey)

def get_wf(run_num: int, channel: int):
    data = read_wf_csv("/Users/yuto/VS/acc_intern/data/osc/e+_run{:0=2}.csv".format(run_num))
    time = data[0]
    Vpp = data[4+channel]
    graph = TPGraph(time.shape[0], time, Vpp)
    return graph

def calc_position_error_propagation(v1, v2, v1_error, v2_error):
    R = R_BPM
    ret = (v1_error*(R*v2) / (v1+v2)**2)**2 + (v2_error*(R*v2) / (v1+v2)**2)**2
    ret = ret ** (1/2)
    return ret

def get_position(v1, v2):
    ret = (R_BPM*(v1-v2)) / (2*(v1+v2))
    return ret
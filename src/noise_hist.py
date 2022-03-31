import ROOT as r
import numpy as np
import sys
import matplotlib.pyplot as plt
from utils import read_wf_csv, calc_channel_sum_error_propagation

NOISE_USE_RANGE = (31.5e-9, 33.5e-9)

def get_noise_error(run_num: int, channel: int):
    data = read_wf_csv('/Users/yuto/VS/acc_intern/data/osc/e+_run{:0=2}.csv'.format(run_num))
    time = data[0]
    voltage = data[4 + channel]
    range_index = np.where((time < NOISE_USE_RANGE[0]) | (NOISE_USE_RANGE[1] < time))
    hist_title = "noise dist. run{}, ch{};voltage [V];intensity".format(run_num, channel)
    canvas = r.TCanvas()
    hist = r.TH1D("noise_{}_{}".format(run_num, channel), hist_title, 300, -15, 15)
    func = r.TF1("noise_func_{}_{}".format(run_num, channel), "gaus", -15, 15)
    for v in voltage[range_index]: hist.Fill(v)
    hist.Fit(func, "R")
    hist.Draw()
    canvas.SaveAs("/Users/yuto/VS/acc_intern/img/noise_hist_run{}_ch{}.png".format(run_num, channel))
    fitted_const = func.GetParameter(0)
    fitted_mean = func.GetParameter(1)
    fitted_sigma = func.GetParameter(2)
    return fitted_const, fitted_mean, fitted_sigma

def get_all_noise_errors():
    ret = []
    for i in range(1, 14):
        errors_chs = tuple(get_noise_error(i, ch)[2] for ch in range(1, 5))
        print(errors_chs)
        error_sum = calc_channel_sum_error_propagation(errors_chs)
        ret.append(error_sum)
    return np.array(ret)

def get_noise_error_by_channel(channel):
    ret = []
    for run_num in range(1, 14):
        _, _, e = get_noise_error(run_num, channel)
        ret.append(e)
    return np.array(ret)

def main():
    r.gROOT.SetBatch()
    for run in range(1, 14):
        for ch in range(1, 5):
            print(get_noise_error(run, ch))

if __name__ == "__main__":
    main()

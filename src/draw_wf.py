import ROOT as r
import csv
import numpy as np
import array
from utils import read_wf_csv, TPGraph


def make_waveform_tgraph(filename: str = '/Users/yuto/VS/acc_intern/data/osc/e+_run01.csv', index = 1, xrange = (0, 1)):
    csv_data = read_wf_csv(filename)
    range_index = np.where((xrange[0] < csv_data[0]) & (csv_data[0] < xrange[1]))
    g = TPGraph(range_index[0].shape[0], csv_data[0][range_index], csv_data[index][range_index])
    g.SetMarkerStyle(1)
    return g

def save_all_waveforms(filename: str = '/Users/yuto/VS/acc_intern/data/osc/e+_run01.csv'):
    canvas = r.TCanvas("", "", 600*2, 600*4)
    graphs = [make_waveform_tgraph(filename, i+1, xrange=(0, 1)) for i in range(12)]
    canvas.Divide(1, 4)
    for i in range(4):
        canvas.cd(i+1)
        graphs[i+4].SetTitle("ch{};time [sec];Voltage [V]".format(i+1))
        graphs[i+4].Draw("AL")
    canvas.SaveAs(filename.replace(".csv", ".png"))
    canvas.SaveAs(filename.replace(".csv", ".root"))

if __name__ == '__main__':
    r.gROOT.SetBatch()
    for i in range(13):
        save_all_waveforms('/Users/yuto/VS/acc_intern/data/osc/e+_run{:0=2}.csv'.format(i+1))
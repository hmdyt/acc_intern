import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
from utils import NAMES, get_position, read_csv, calibration_function, TPGraphErrors
from noise_hist import get_all_noise_errors

def draw_charge_by_particle(particle="electron"):
    if particle=="electron":
        data_arg = "vpp1_ch{}"
    elif particle=="positron":
        data_arg = "vpp2_ch{}"
    else:
        print("invalid argument")
        exit()

    csv_data = read_csv()
    phase = csv_data['phase']
    Vpp_sum = sum([csv_data[data_arg.format(i+1)] for i in range(4)])
    Vpp_sum_error = get_all_noise_errors()
    charge = calibration_function(Vpp_sum)
    charge_error= calibration_function(Vpp_sum_error)
    n_points = phase.shape[0]
    graph = TPGraphErrors(n_points, phase, charge, [0 for _ in range(n_points)], charge_error)
    return graph

def draw_charge():
    graph_electron = draw_charge_by_particle("electron")
    graph_positron = draw_charge_by_particle("positron")
    graph_electron.SetMarkerStyle(21)
    graph_positron.SetMarkerStyle(21)
    graph_electron.SetMarkerColor(4)
    graph_positron.SetMarkerColor(2)
    legend = r.TLegend(0.8, 0.85, 0.95, 0.95)
    legend.AddEntry(graph_electron, "electron")
    legend.AddEntry(graph_positron, "positron")
    canvas = r.TCanvas()
    axis = r.TH2D("axis", "phase vs charge;phase [degree];charge [C]", 0, 75, 475, 0, 0, 5e-9)
    axis.SetStats(0)
    axis.Draw("AXIS")
    axis.GetXaxis().SetTitleSize(0.06)
    axis.GetXaxis().SetTitleOffset(0.6)
    axis.GetYaxis().SetTitleSize(0.06)
    axis.GetYaxis().SetTitleOffset(0.6)
    graph_electron.Draw("P SAME")
    graph_positron.Draw("P SAME")
    legend.Draw()
    canvas.SaveAs("/Users/yuto/VS/acc_intern/img/charge_e+e-.png")
    canvas.SaveAs("/Users/yuto/VS/acc_intern/img/charge_e+e-.svg")

def main():
    r.gROOT.SetBatch()
    draw_charge()

if __name__ == "__main__":
    main()
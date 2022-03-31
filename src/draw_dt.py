import ROOT as r
import numpy as np
from utils import read_csv, TPGraph

def draw_dt():
    data = read_csv()
    phase = data["phase"]
    dt_ave = sum([data["dt_ch{}".format(ch)] for ch in range(1, 5)]) / 4
    canvas = r.TCanvas()
    graph = TPGraph(phase.shape[0], phase, dt_ave)
    graph.SetTitle("phase vs dt;phase [degree];dt [ps]")
    graph.SetMarkerStyle(8)
    graph.Draw("AP")
    graph.GetXaxis().SetTitleSize(0.06)
    graph.GetXaxis().SetTitleOffset(0.6)
    graph.GetYaxis().SetTitleSize(0.06)
    graph.GetYaxis().SetTitleOffset(0.6)
    canvas.SaveAs("/Users/yuto/VS/acc_intern/img/dt.png")
    canvas.SaveAs("/Users/yuto/VS/acc_intern/img/dt.svg")

def main():
    r.gROOT.SetBatch()
    draw_dt()

if __name__ == "__main__":
    main()
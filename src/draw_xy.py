from calendar import c
import ROOT as r
from utils import read_csv, get_position, calc_position_error_propagation, TPGraphErrors
from noise_hist import get_noise_error_by_channel

def get_xy_graph(xy="x", particle="electron"):
    if xy == "x":
        tar_ch = (1, 3)
    elif xy =="y":
        tar_ch = (2, 4)
    else:
        print("invalid argument")
        exit()
    if particle == "electron":
        tar_Vpp = "vpp1_ch{}"
    elif particle == "positron":
        tar_Vpp = "vpp2_ch{}"
    
    data = read_csv()
    phase = data["phase"]
    v1 = data[tar_Vpp.format(tar_ch[0])]
    v2 = data[tar_Vpp.format(tar_ch[1])]
    v1_error = get_noise_error_by_channel(tar_ch[0])
    v2_error = get_noise_error_by_channel(tar_ch[1])
    pos_xy = get_position(v1, v2)
    pos_xy_error = calc_position_error_propagation(v1, v2, v1_error, v2_error)
    
    n_points = phase.shape[0]
    graph = TPGraphErrors(n_points, phase, pos_xy, [0 for _ in range(n_points)], pos_xy_error)
    graph.SetTitle("{} {} ch={};phase [degree];{} [mm]".format(particle, xy, tar_ch, xy))
    graph.SetMarkerStyle(8)
    return graph

def make_xy_graph(xy, particle):
    canvas = r.TCanvas()
    g = get_xy_graph(xy, particle)
    g.Draw("AP")
    g.GetXaxis().SetTitleSize(0.06)
    g.GetXaxis().SetTitleOffset(0.6)
    g.GetYaxis().SetTitleSize(0.06)
    g.GetYaxis().SetTitleOffset(0.6)
    canvas.SaveAs("img/position_{}_{}.png".format(particle, xy))
    
def main():
    r.gROOT.SetBatch()
    for particle in ["electron", "positron"]:
        for xy in ["x", "y"]:
            make_xy_graph(xy, particle)


if __name__ == "__main__":
    main()
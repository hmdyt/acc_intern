from draw_xy import get_xy_graph
from utils import TPGraphErrors
import ROOT as r

def get_pos(xy = "x", particle = "electron"):
    graph = get_xy_graph(xy, particle)
    n_points = graph.GetN()
    pos = list(graph.GetY())
    pos_error = []
    for i in range(n_points):
        pos_error.append(graph.GetErrorY(i))
    return pos, pos_error    

def get_xy_scatter_graph(particle="electron"):
    pos_x, pos_x_error = get_pos("x", particle)
    pos_y, pos_y_error = get_pos("y", particle)
    n_points = len(pos_x)
    graph = TPGraphErrors(n_points, pos_x, pos_y, pos_x_error, pos_y_error)
    graph.SetMarkerStyle(8)
    graph.SetMarkerColor(4 if particle == "electron" else 2)
    return graph

def main():
    r.gROOT.SetBatch()
    canvas = r.TCanvas("", "", 1000, 1000)
    graph_positron = get_xy_scatter_graph("positron")
    graph_electron = get_xy_scatter_graph("electron")
    axis = r.TH2D("xy_scatter", "beam position;x [mm];y [mm]", 0, -7, 7, 0, -7, 7)
    axis.SetStats(0)
    axis.Draw("AXIS")
    graph_electron.Draw("P SAME")
    graph_positron.Draw("P SAME")
    canvas.SaveAs("/Users/yuto/VS/acc_intern/img/xy_scatter.png")
    canvas.SaveAs("/Users/yuto/VS/acc_intern/img/xy_scatter.svg")

if __name__ == "__main__":
    main()
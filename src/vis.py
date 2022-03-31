from cProfile import label
from typing import Dict, List
import matplotlib.pyplot as plt
import numpy as np
import time
import multiprocessing

FILE_MANE = "data/test01.csv"
OUTPUT_PATH = "img/test01.jpg"
NAMES = [
    "phase",
    "dt_ch1", "vpp1_ch1", "vpp2_ch1",
    "dt_ch2", "vpp1_ch2", "vpp2_ch2",
    "dt_ch3", "vpp1_ch3", "vpp2_ch3",
    "dt_ch4", "vpp1_ch4", "vpp2_ch4"
]
INTERVAL_SEC = 5

def read_csv(file: str, names: List[str]) -> Dict[str, List[float]]:
    data = {name: [] for name in names}
    with open(file, 'r') as f:
        for line in f.read().split('\n'):
            if line[0] == '#': continue
            if len(line.split(',')) != 13:
                print("parse error\n current line length is {}".format(len(line.split(','))))
                exit()
            line_splited = line.replace(' ', '').split(',')
            for i in range(len(names)):
                data[names[i]].append(float(line_splited[i]))
    return data

def remake_phase(data):
    for i in range(len(data["phase"])):
        data["phase"][i] %= 360
    return data

def plot_data(data: Dict[str, List[float]]) -> None:
    fig = plt.figure(figsize=(6.4*2.2, 4.8*2.2))
    ax = [fig.add_subplot(2, 2, i+1) for i in range(4)]
    dt_ave = [
        (data['dt_ch1'][i] + data['dt_ch2'][i] + data['dt_ch3'][i] + data['dt_ch4'][i]) / 4
        for i in range(len(data['phase']))
    ]
    vpp1_ave = [
        (data['vpp1_ch1'][i] + data['vpp1_ch2'][i] + data['vpp1_ch3'][i] + data['vpp1_ch4'][i]) / 4
        for i in range(len(data['phase']))
    ]
    vpp2_ave = [
        (data['vpp2_ch1'][i] + data['vpp2_ch2'][i] + data['vpp2_ch3'][i] + data['vpp2_ch4'][i]) / 4
        for i in range(len(data['phase']))
    ]
    ax[0].scatter(data['phase'], vpp1_ave, label='ave', marker='x')
    ax[1].scatter(data['phase'], vpp2_ave, label='ave', marker='x')
    ax[2].scatter(data['phase'], dt_ave, label='ave', marker='x')
    for i in range(4):
        dt_name = 'dt_ch{}'.format(i+1)
        vpp1_name = 'vpp1_ch{}'.format(i+1)
        vpp2_name = 'vpp2_ch{}'.format(i+1)
        channel = 'ch{}'.format(i+1)
        ax[0].scatter(data['phase'], data[vpp1_name], label=channel)
        ax[1].scatter(data['phase'], data[vpp2_name], label=channel)
        ax[2].scatter(data['phase'], data[dt_name], label=channel)
    
    for i in range(4): ax[i].legend()
    ax[0].set_title("Vpp1 (electron)")
    ax[0].set_xlabel("phase [degree]")
    ax[0].set_ylabel("Vpp1 [V]")
    ax[1].set_title("Vpp2 (positron)")
    ax[1].set_xlabel("phase [degree]")
    ax[1].set_ylabel("Vpp2 [V]")
    ax[2].set_title("dt")
    ax[2].set_xlabel("phase [degree]")
    ax[2].set_ylabel("dt [ps]")
    fig.savefig(OUTPUT_PATH)
    plt.clf()
    plt.close()

def main():
    data = read_csv(FILE_MANE, NAMES)
    #data = remake_phase(data)
    plot_data(data)
    time.sleep(INTERVAL_SEC)

if __name__ == '__main__':
    main()
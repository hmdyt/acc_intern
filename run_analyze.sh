#! /usr/bin/env bash

python src/draw_charge.py & 
python src/draw_dt.py &
python src/draw_xy.py &
python src/draw_xy_scatter.py &
python src/draw_wf.py

open /Users/yuto/VS/acc_intern/img/charge_e+e-.png
open /Users/yuto/VS/acc_intern/img/dt.png
open /Users/yuto/VS/acc_intern/img/position_*.png
open /Users/yuto/VS/acc_intern/img/xy_scatter.png
open /Users/yuto/VS/acc_intern/data/osc/e+_run[0-9][0-9].png


echo "DONE"
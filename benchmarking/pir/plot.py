from pir import cal_pir_tput
from pirac import cal_pirac_tput

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import numpy as np
import argparse
import itertools
import pandas as pd

import utils

###########################
# PLOT PARAMETERS
###########################
TINY_SIZE = 8
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12
matplotlib.rcParams['font.family'] = 'serif'
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=TINY_SIZE)     # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rc('hatch', linewidth=0.5)

# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Create plots for the paper')
parser.add_argument('-exp','--expType', choices=["es", "batch"],
                     required=True, type=str,
                     help='What type of plot to plot')
parser.add_argument('-bv','--batchValues', nargs='+',
                     required=False, type=int, default=[1,5,10,20],
                     help='Batch values to run experiment on.')
parser.add_argument('-p','--pirName', default="spiralstreampack",
                     required=False, type=str,
                     help='PIR scheme to run batch experiments')
parser.add_argument('-f','--figName',
                     required=False, type=str,
                     help='Name of the saved image')


def gen_elem_comp_plot(fig_name):
    """
    NOTE: Don't rerun the experiment due to high latency
    """
    PIR_NAMES = ["spiralpir","spiralstreampack", "sealpir"]
    PIR_LABELS = ["SpiralPIR", "SpiralStreamPack", "SealPIR"] #, "FastPIR"]
    PIRAC_MODES = ["bl", "mp", "fs"]

    def generate_results(log2_db_size, elem_sizes, verbose=False):
        df_all = utils.concatenate_jsons("results/data", verbose)
        
        # create new dataframe with only those rows corresponding to elem_sizes
        df_es = df_all[(df_all['log2_db_size'] == log2_db_size)
                                & (df_all['elem_size'].isin(elem_sizes))]
        assert len(df_es)==len(elem_sizes)

        tput_columns = [f"{pir_name}_{pirac_mode}_tput" for pir_name in PIR_NAMES
                                                        for pirac_mode in PIRAC_MODES]
        col_filter = ["elem_size"]+tput_columns
        df_col = df_es[col_filter]
        assert len(PIR_NAMES)*len(PIRAC_MODES)==sum(['tput' in col for col in df_col.columns])

        if verbose:
            print(df_col)
        return df_col

    # get results
    results = generate_results(utils.LOG2_DB_SIZE, utils.ELEM_SIZES)
    x_values = results["elem_size"].values

    # set image scale
    plt.figure()
    plt.yscale("log")
    plt.xscale("log")

    colors = ['#08519c', '#ff7f00', '#16a085', '#8e44ad'] #, '#c0392b', '#333']
    cc = itertools.cycle(colors)
    plot_lines = []

    for pir in PIR_NAMES:
        c = next(cc)
        l1, = plt.plot(x_values, results[f'{pir}_bl_tput'].values, color=c, linestyle='-',  alpha=0.7)
        l2, = plt.plot(x_values, results[f'{pir}_mp_tput'].values, color=c, linestyle='--')
        l3, = plt.plot(x_values, results[f'{pir}_fs_tput'].values, color=c, linestyle=':')
        plot_lines.append([l1, l2, l3])
    
    
    legend1 = plt.legend([l[0] for l in plot_lines], PIR_LABELS, loc="upper left")
    legend2 = plt.legend(plot_lines[0], ["Baseline", "With MP", "With FS"], loc="lower right")
    plt.gca().add_artist(legend1)
    plt.gca().add_artist(legend2)

    plt.xlabel("Entry size (in bytes)")
    plt.ylabel("Throughput (in MB/s)")

    plt.tight_layout()
    plt.savefig(f"images/{fig_name}.pdf", dpi=300)
    print(f"Successfully generated and save the plot with name {fig_name}")

def gen_batched_bar_plot(pir_name, batch_values, fig_name):
    plt.figure().set_figheight(3)

    # calculate tputs
    log_db_size = utils.LOG2_DB_SIZE
    elem_size = (1<<15)
    pir_tput = cal_pir_tput(pir_name, log_db_size, elem_size, {}, False, num_iter=5)
    re_tput = cal_pirac_tput(log_db_size, elem_size,  5, rekeying = False)
    pirac_tput = cal_pirac_tput(log_db_size, elem_size,  5, rekeying = True)
    
    # calculate batch tputs
    pir_tputs = []
    re_tputs = []
    pirac_tputs = []
    for bv in batch_values:
        pir_tputs.append(pir_tput)
        re_tputs.append(utils.cal_tput_with_pirac(pir_tput, re_tput, bv))
        pirac_tputs.append(utils.cal_tput_with_pirac(pir_tput, pirac_tput, bv))
    # set the width of each bar and colors
    barWidth = 0.25
    colors = ['#08519c', '#ff7f00', '#16a085', '#8e44ad', '#c0392b', '#333']

    # set the position of each group on the x-axis
    pir_positions = np.arange(len(batch_values))
    re_positions = [x + barWidth for x in pir_positions]
    pirac_positions = [x + barWidth for x in re_positions]
    
    # create the bar graph
    plt.bar(pir_positions, pir_tputs, color=colors[0], width=barWidth, edgecolor='white', label="Baseline",  hatch='////')
    plt.bar(re_positions, re_tputs, color=colors[1], width=barWidth, edgecolor='white', label="With MP",  hatch='////')
    plt.bar(pirac_positions, pirac_tputs, color=colors[2], width=barWidth, edgecolor='white', label="With FS",  hatch='////')
    
    # add xticks on the middle of the group bars
    plt.xticks([i + barWidth for i in range(len(batch_values))], batch_values)

    # add a legend
    plt.legend(loc="lower right") # bbox_to_anchor=(0.1, 1.0)

    plt.xlabel("Number of batched entries (T)")
    plt.ylabel("Throughput (MB/s)")

    # save the plot
    plt.tight_layout()
    plt.savefig(f"images/{fig_name}.pdf", dpi=300)

if __name__ == "__main__":
    args = parser.parse_args()
    exp = args.expType
    bv = args.batchValues
    pir_name = args.pirName
    fig_name = args.figName
    
    if exp=="es":
        fig_name = "comparision_elem_sizes" if fig_name is None else fig_name
        gen_elem_comp_plot(fig_name)
    elif exp=="batch":
        fig_name = "batched_opt" if fig_name is None else fig_name
        gen_batched_bar_plot(pir_name, bv, fig_name)
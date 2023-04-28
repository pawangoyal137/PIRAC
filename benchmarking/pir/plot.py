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

def generate_results(log2_db_size, elem_sizes, tput_columns, verbose=False):
    df_all = utils.concatenate_jsons("results/data", verbose)
    
    # create new dataframe with only those rows corresponding to elem_sizes
    df_es = df_all[(df_all['log2_db_size'] == log2_db_size)
                            & (df_all['elem_size'].isin(elem_sizes))]
    assert len(df_es)==len(elem_sizes)

    col_filter = ["elem_size"]+tput_columns
    df_col = df_es[col_filter]

    if verbose:
        print(df_col)
    return df_col

def gen_elem_comp_plot(fig_name):
    """
    NOTE: Don't rerun the experiment due to high latency
    """
    PIR_NAMES = ["spiralpir","spiralstreampack", "sealpir", "fastpir"]
    PIR_LABELS = ["SpiralPIR", "SpiralStreamPack", "SealPIR", "FastPIR"]
    PIRAC_MODES = ["bl", "mp", "fs"]

    # get results
    tput_columns = [f"{pir_name}_{pirac_mode}_tput" for pir_name in PIR_NAMES
                                                    for pirac_mode in PIRAC_MODES]
    results = generate_results(utils.LOG2_DB_SIZE, utils.ELEM_SIZES, tput_columns)
    x_values = results["elem_size"].values

    # create a 2 by 1 figure
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=False)

    # set fig height 
    fig.set_figheight(6)

    # set figure scale
    ax1.set_yscale("log")
    ax1.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xscale("log")
    # plt.grid(True, linewidth=1, color='grey', alpha=0.5)


    colors = ['#08519c', '#ff7f00', '#16a085', '#8e44ad'] #, '#c0392b', '#333']
    cc = itertools.cycle(colors)
    plot_lines = []

    for pir in PIR_NAMES:
        c = next(cc)
        l1, = ax1.plot(x_values, results[f'{pir}_bl_tput'].values, linewidth=2, color=c, linestyle='-', label=pir) #, marker='o', markersize=4)
        l2, = ax1.plot(x_values, results[f'{pir}_mp_tput'].values, linewidth=2, color=c, linestyle='--')
        l3, = ax2.plot(x_values, results[f'{pir}_bl_tput'].values, linewidth=2, color=c, linestyle='-') #, marker='o', markersize=4)
        l4, = ax2.plot(x_values, results[f'{pir}_fs_tput'].values, linewidth=2, color=c, linestyle=':')
        plot_lines.append([l1, l2, l3, l4])
    

    # set labels, x axis is common
    ax1.set_ylabel("Throughput (in MB/s)")
    ax2.set_xlabel("Entry size (in bytes)")
    ax2.set_ylabel("Throughput (in MB/s)")

    # use tight layout to avoid any empty side spaces
    fig.tight_layout()

    #create space for legend at the bottom and add the legend
    ax1.legend(plot_lines[0][:2], ["Baseline (& Pirac w/ basic auth)", "Pirac w/ metadata-private auth"],
                          loc="lower right", framealpha=1)
    ax2.legend(plot_lines[0][2:], ["Baseline (& Pirac w/ basic auth)", "Pirac w/ forward-secret auth"],
                          loc="lower right", framealpha=1)
    plt.subplots_adjust(bottom=0.14)
    handles, _ = ax1.get_legend_handles_labels()
    fig.legend(handles, PIR_LABELS, loc="lower left", ncol=len(PIR_LABELS), 
                                    bbox_to_anchor=(0.1, 0), framealpha=1)
    
    # save the figure
    fig.savefig(f"images/{fig_name}.pdf", dpi=300)
    print(f"Successfully generated and save the plot with name {fig_name}")

def gen_batched_bar_plot(pir_name, batch_values, fig_name):
    PIR_NAME = "spiralstreampack"
    tput_columns = [f"{PIR_NAME}_{pm}_tput" for pm in ["bl", "mp", "fs"]]
    results = generate_results(utils.LOG2_DB_SIZE, [1<<15], tput_columns, verbose=False)
    
    # calculate tputs
    pir_tput = results[f'{PIR_NAME}_bl_tput'].values[0]
    pir_mp_tput = results[f'{PIR_NAME}_mp_tput'].values[0]
    pir_fs_tput = results[f'{PIR_NAME}_fs_tput'].values[0]
    
    # calculate batch tputs
    pir_tputs = []
    re_tputs = []
    pirac_tputs = []
    for bv in batch_values:
        pir_tputs.append(pir_tput)
        re_tputs.append(utils.cal_tput_for_comb(pir_tput, pir_mp_tput, bv))
        pirac_tputs.append(utils.cal_tput_for_comb(pir_tput, pir_fs_tput, bv))
    # set the width of each bar and colors
    barWidth = 0.25
    colors = ['#08519c', '#ff7f00', '#16a085', '#8e44ad', '#c0392b', '#333']

    # set the position of each group on the x-axis
    pir_positions = np.arange(len(batch_values))
    re_positions = [x + barWidth for x in pir_positions]
    pirac_positions = [x + barWidth for x in re_positions]
    
    # set figure height
    plt.figure().set_figheight(3)

    # create the bar graph
    plt.bar(pir_positions, pir_tputs, color=colors[0], width=barWidth,
         edgecolor='white', label="Baseline (& Pirac w/ basic auth)",  hatch='////')
    plt.bar(re_positions, re_tputs, color=colors[1], width=barWidth,
         edgecolor='white', label="Pirac w/ metadata-private auth",  hatch='////')
    plt.bar(pirac_positions, pirac_tputs, color=colors[2], width=barWidth,
         edgecolor='white', label="Pirac w/ forward-secret auth",  hatch='////')
    
    # add xticks on the middle of the group bars
    plt.xticks([i + barWidth for i in range(len(batch_values))], batch_values)

    # add a legend
    plt.legend(loc="lower right") # bbox_to_anchor=(0.1, 1.0)

    plt.xlabel("Number of queries between re-keying or re-encryption (T)")
    plt.ylabel("Throughput (MB/s) \n (amortized over T queries)")

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
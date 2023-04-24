from pir import cal_pir_tput
from pirac import cal_pirac_tput
from concat import concat

import matplotlib
matplotlib.use("TKAgg")
print(matplotlib.get_backend())
import matplotlib.pyplot as plt
import os
import numpy as np
import argparse
import itertools

import utils

DATA_DIRECTORY = "results/data"

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
# plt.rcParams['savefig.dpi'] = 300

# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Run evaluation by comparing\
                                            different schemes')
parser.add_argument('-ds','--dbSize',
                     required=False, type=int,
                     help='Log 2 Database size to run experiment on.')
parser.add_argument('-es','--elemSizes', nargs='+',
                     required=False, type=int,
                     help='Element sizes (in bits) to run experiment on.')
parser.add_argument('-x','--xLabel',
                     required=False, type=str,
                     help='X label for the plot')
parser.add_argument('-f','--figName',
                     required=False, type=str,
                     help='Name of the saved image')

# def get_results(pir_names, elem_sizes, pirac_modes, run_fresh=False, verbose=False):
#     df_all = concat(DATA_DIRECTORY)

#     # create new dataframe with only those rows corresponding to elem_sizes
#     df_es = df_all[(df_all['log2_db_size'] == utils.LOG2_DB_SIZE) & (df_all['elem_size'].isin(elem_sizes))]
#     assert len(df_es)==len(elem_sizes)

#     tput_columns = [f"{pir_name}_{pirac_mode}_tput" for pir_name in pir_names 
#                                                     for pirac_mode in pirac_modes]
#     col_filter = ["elem_size"]+tput_columns
#     df_col = df_es[col_filter]
#     assert len(pir_names)*len(pirac_modes)==sum(['tput' in col for col in df_col.columns])

#     if verbose:
#         print(df_col)
#     return df_col

# def run_PIRs(log2_db_sizes, elem_sizes):
#     owd = os.getcwd()
#     results = {}

#     # os.chdir(SimplePirPath)
#     # results["simplepir"] = benchmark_SimplePir(log2_db_sizes, elem_sizes)
#     # results["simplepir_offline_include"] = benchmark_SimplePir(log2_db_sizes, elem_sizes, True)

#     os.chdir(owd)
#     os.chdir(utils.SpiralPirPath)
#     results["spiralpir"] = benchmark_SpiralPir(log2_db_sizes, elem_sizes)
#     results["spiralpir_stream_pack"] = benchmark_SpiralPir(log2_db_sizes, elem_sizes, stream=True, pack=True)

#     os.chdir(owd)
#     os.chdir(utils.SealPirPath)
#     results["sealpir"] = benchmark_SealPir(log2_db_sizes, elem_sizes)

#     os.chdir(owd)
#     os.chdir(utils.FastPirPath)
#     results["fastpir"] = benchmark_FastPir(log2_db_sizes, elem_sizes)
    
#     os.chdir(owd)
#     results["tier2"] = benchmark_pirac(log2_db_sizes, elem_sizes, num_iter=5, rekeying=False)
#     results["tier3"] = benchmark_pirac(log2_db_sizes, elem_sizes, num_iter=5, rekeying=True)
    
#     return results


def gen_save_plot(results, x_values, fig_name):
    plt.figure()
    plt.yscale("log")
    plt.xscale("log")

    schemes = ["spiralpir", "spiralpir_stream_pack", "sealpir", "fastpir"]
    colors = ['#08519c', '#ff7f00', '#16a085', '#8e44ad'] #, '#c0392b', '#333']
    cc = itertools.cycle(colors)
    plot_lines = []

    for scheme in schemes:
        tput_with_tier2 = utils.cal_tput_with_pirac(results[scheme], results["tier2"])
        tput_with_tier3 = utils.cal_tput_with_pirac(results[scheme], results["tier3"])
        c = next(cc)
        l1, = plt.plot(x_values, results[scheme], color=c, linestyle='-',  alpha=0.7)
        l2, = plt.plot(x_values, tput_with_tier2, color=c, linestyle='--')
        l3, = plt.plot(x_values, tput_with_tier3, color=c, linestyle=':')
        plot_lines.append([l1, l2, l3])
    
    scheme_labels = ["SpiralPIR", "SpiralStreamPack", "SealPIR", "FastPIR"]
    legend1 = plt.legend([l[0] for l in plot_lines], scheme_labels, loc="upper left")
    legend2 = plt.legend(plot_lines[0], ["Basic", "With MP", "With MP+FS"], loc="upper right")
    plt.gca().add_artist(legend1)
    plt.gca().add_artist(legend2)

    plt.xlabel("Entry size (in bytes)")
    plt.ylabel("Throughput (in MB/s)")

    plt.tight_layout()
    plt.savefig(f"images/{fig_name}.pdf", dpi=300)
    print(f"Successfully generated and save the plot with name {fig_name}")

def gen_batched_bar_plot(pir_name, x_values, fig_name):
    pir_tput = cal_pir_tput(pir_name, utils.LOG2_DB_SIZE, utils.ELEM_SIZE, {}, False)
    re_tput = cal_pirac_tput(utils.LOG2_DB_SIZE, utils.ELEM_SIZE,  10, rekeying = False)
    pirac_tput = cal_pirac_tput(utils.LOG2_DB_SIZE, utils.ELEM_SIZE,  10, rekeying = True)

    groups = []
    # create data for three bar lines per group
    for k in x_values:
        group = [pir_tput, 
                utils.cal_tput_with_pirac(pir_tput, re_tput, k),
                utils.cal_tput_with_pirac(pir_tput, pirac_tput, k)]
        groups.append(group)

    # set the width of each bar and colors
    barWidth = 0.25
    colors = ['#08519c', '#ff7f00', '#16a085', '#8e44ad', '#c0392b', '#333']

    # set the position of each group on the x-axis
    group_positions = [np.arange(len(groups[0]))]
    for i in range(1, len(groups)):
        r = [x + barWidth for x in group_positions[i-1]]
        group_positions.append(r)

    # create the bar graph
    for i in range(len(groups)):
        plt.bar(group_positions[i], groups[i], color=colors[i], width=barWidth, edgecolor='white', label=x_values[i])
    
    # add xticks on the middle of the group bars
    plt.xlabel('k')
    plt.xticks([i + barWidth for i in range(len(groups))], x_values)

    # add a legend
    plt.legend()

    # save the plot
    plt.tight_layout()
    plt.savefig(f"images/bar_plot.pdf", dpi=300)

if __name__ == "__main__":
    args = parser.parse_args()
    log2_db_size = args.dbSize
    elem_sizes = args.elemSizes
    fig_name = args.figName
    
    log2_db_sizes = [utils.LOG2_DB_SIZE] if log2_db_size is None else [log2_db_size]
    elem_sizes = utils.ELEM_SIZES if elem_sizes is None else elem_sizes
    fig_name = "comparision_elem_sizes" if fig_name is None else fig_name
    x_values = [e//8 for e in elem_sizes]
    
    # results = run_PIRs(log2_db_sizes, elem_sizes)
    gen_batched_bar_plot("spiralpir", x_values, fig_name)

    # get_results(["spiralpir"], [128, 512], ["mp", "fs"], run_fresh=False)
from eval_pirac import benchmark_pirac
from eval_simplepir import benchmark_SimplePir
from eval_spiralpir import benchmark_SpiralPir
from eval_sealpir import benchmark_SealPir
from eval_fastpir import benchmark_FastPir
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
import argparse
import itertools

import utils

###########################
# PLOT PARAMETERS
###########################
TINY_SIZE = 7
SMALL_SIZE = 7
MEDIUM_SIZE = 8
BIGGER_SIZE = 10
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
parser.add_argument('-e','--expType', choices=['ds', 'es'],
                     required=True, type=str,
                     help='Tells file if to run db_size or elem_size experiments')
parser.add_argument('-ds','--dbSizes', nargs='+',
                     required=False, type=int,
                     help='Log 2 Database sizes to run experiment on.')
parser.add_argument('-es','--elemSizes', nargs='+',
                     required=False, type=int,
                     help='Element sizes (in bits) to run experiment on.')
parser.add_argument('-x','--xLabel',
                     required=False, type=str,
                     help='X label for the plot')
parser.add_argument('-f','--figName',
                     required=False, type=str,
                     help='Name of the saved image')

def run_PIRs(log2_db_sizes, elem_sizes):
    owd = os.getcwd()
    results = {}

    # os.chdir(SimplePirPath)
    # results["simplepir"] = benchmark_SimplePir(log2_db_sizes, elem_sizes)
    # results["simplepir_offline_include"] = benchmark_SimplePir(log2_db_sizes, elem_sizes, True)

    os.chdir(owd)
    os.chdir(utils.SpiralPirPath)
    results["spiralpir"] = benchmark_SpiralPir(log2_db_sizes, elem_sizes)
    results["spiralpir_stream_pack"] = benchmark_SpiralPir(log2_db_sizes, elem_sizes, stream=True, pack=True)

    os.chdir(owd)
    os.chdir(utils.SealPirPath)
    results["sealpir"] = benchmark_SealPir(log2_db_sizes, elem_sizes)

    os.chdir(owd)
    os.chdir(utils.FastPirPath)
    results["fastpir"] = benchmark_FastPir(log2_db_sizes, elem_sizes)
    
    os.chdir(owd)
    results["tier2"] = benchmark_pirac(log2_db_sizes, elem_sizes, num_iter=5, rekeying=False)
    results["tier3"] = benchmark_pirac(log2_db_sizes, elem_sizes, num_iter=5, rekeying=True)
    
    return results

def gen_save_plot(results, x_values, x_label, fig_name):
    plt.figure()
    plt.yscale("log")

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
    legend1 = plt.legend([l[0] for l in plot_lines], scheme_labels, loc=2)
    legend2 = plt.legend(plot_lines[0], ["Basic", "With MP", "With MP+FS"], loc=4)
    plt.gca().add_artist(legend1)
    plt.gca().add_artist(legend2)

    plt.xlabel(x_label)
    plt.ylabel("Throughput (in MB/s)")
    plt.tight_layout()
    plt.savefig(f"images/{fig_name}.pdf", dpi=300)
    print(f"Successfully generated and save the plot with name {fig_name}")

if __name__ == "__main__":
    args = parser.parse_args()
    exp_type = args.expType
    log2_db_sizes = args.dbSizes
    elem_sizes = args.elemSizes
    x_label = args.xLabel
    fig_name = args.figName
    
    if exp_type=="ds":
        log2_db_sizes = utils.LOG2_DB_SIZES if log2_db_sizes is None else log2_db_sizes
        elem_sizes = [utils.ELEM_SIZE] if elem_sizes is None else elem_sizes
        x_label = "Log2 of Number of Database entries" if x_label is None else x_label
        fig_name = "comparision_db_sizes" if fig_name is None else fig_name
        x_values = log2_db_sizes
    elif exp_type=="es":
        log2_db_sizes = [utils.LOG2_DB_SIZE] if log2_db_sizes is None else log2_db_sizes
        elem_sizes = utils.ELEM_SIZES if elem_sizes is None else elem_sizes
        x_label = "Log2 of Entry size (in bits)" if x_label is None else x_label
        fig_name = "comparision_elem_sizes" if fig_name is None else fig_name
        x_values = np.log2(elem_sizes)
    else:
        raise Exception("Shouldn't reach here")

    assert ((len(elem_sizes)==1) and (exp_type=="ds")) or \
            ((len(log2_db_sizes)==1) and (exp_type=="es"))
    
    results = run_PIRs(log2_db_sizes, elem_sizes)
    gen_save_plot(results, x_values, x_label, fig_name)
from pir import cal_pir_tput
from pirac import cal_pirac_tput

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import numpy as np
import argparse
import itertools

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
# plt.rcParams['savefig.dpi'] = 300

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

    def generate_results(log2_db_sizes, elem_sizes):
        results = {"spiralpir":[],
                "spiralstreampack":[],
                "sealpir":[],
                "fastpir":[],
                "re":[],
                "pirac":[]}

        for log2_db_size in log2_db_sizes:
            for elem_size in elem_sizes:
                results["spiralpir"].append(cal_pir_tput("spiralpir", log2_db_size, elem_size))
                results["spiralpirstreampack"].append(cal_pir_tput("spiralpirstreampack", log2_db_size, elem_size))
                results["sealpir"].append(cal_pir_tput("sealpir", log2_db_size, elem_size))
                results["fastpir"].append(cal_pir_tput("fastpir", log2_db_size, elem_size))
                results["re"] = cal_pirac_tput(log2_db_size, elem_size, num_iter=5, rekeying=False)
                results["pirac"] = cal_pirac_tput(log2_db_size, elem_size, num_iter=5, rekeying=True)
        
        return results

    # get results
    results = generate_results(utils.LOG2_DB_SIZES, utils.ELEM_SIZES)
    x_values = utils.ELEM_SIZES

    # set image scale
    plt.figure()
    plt.yscale("log")
    plt.xscale("log")

    schemes = ["spiralpir", "spiralpirstreampack", "sealpir", "fastpir"]
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
    legend2 = plt.legend(plot_lines[0], ["Basic", "With MP", "With FS"], loc="upper right")
    plt.gca().add_artist(legend1)
    plt.gca().add_artist(legend2)

    plt.xlabel("Entry size (in bytes)")
    plt.ylabel("Throughput (in MB/s)")

    plt.tight_layout()
    plt.savefig(f"images/{fig_name}.pdf", dpi=300)
    print(f"Successfully generated and save the plot with name {fig_name}")

def gen_batched_bar_plot(pir_name, batch_values, fig_name):
    plt.figure()

    # calculate tputs
    log_db_size = 20 #utils.LOG2_DB_SIZE
    elem_size = (1<<15)
    pir_tput = cal_pir_tput(pir_name, log_db_size, elem_size, {}, False, num_iter=1)
    re_tput = cal_pirac_tput(log_db_size, elem_size,  5, rekeying = False)
    pirac_tput = cal_pirac_tput(log_db_size, elem_size,  5, rekeying = True)
    
    # calculate batch tputs
    re_tputs = []
    pirac_tputs = []
    for bv in batch_values:
        re_tputs.append(pir_tput / utils.cal_tput_with_pirac(pir_tput, re_tput, bv))
        pirac_tputs.append(pir_tput / utils.cal_tput_with_pirac(pir_tput, pirac_tput, bv))
    print(re_tputs, pirac_tputs)
    # set the width of each bar and colors
    barWidth = 0.33
    colors = ['#08519c', '#ff7f00', '#16a085', '#8e44ad', '#c0392b', '#333']

    # set the position of each group on the x-axis
    re_positions = np.arange(len(batch_values))
    pirac_positions = [x + barWidth for x in re_positions]
    
    # create the bar graph
    plt.bar(re_positions, re_tputs, color=colors[0], width=barWidth, edgecolor='white', label="With MP",  hatch='////')
    plt.bar(pirac_positions, pirac_tputs, color=colors[1], width=barWidth, edgecolor='white', label="With FS",  hatch='////')
    
    # add xticks on the middle of the group bars
    plt.xticks([i + 0.5*barWidth for i in range(len(batch_values))], batch_values)

    # add a legend
    plt.legend(loc="upper right")

    plt.xlabel("Number of batched entries")
    plt.ylabel("Overhead (compared to baseline)")

    # set y scale
    plt.ylim(0, 2.5)
    plt.yticks(ticker.MultipleLocator(0.5).tick_values(0.5, 2.0))
    plt.yticks(ticker.MultipleLocator(.25).tick_values(0.25, 2.25), minor=True)

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
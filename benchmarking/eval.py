from eval_pirac import benchmark_pirac
from eval_simplepir import benchmark_SimplePir
from eval_spiralpir import benchmark_SpiralPir
import matplotlib.pyplot as plt
import os
import numpy as np
import argparse

# plt.style.use('seaborn')

# declare the paths for the other PIR schemes
SimplePirPath = "../simplepir/pir"
SpiralPirPath = "../../spiral"

# declare the constants/ defaults for the experiments
LOG2_DB_SIZE = 16
ELEM_SIZE = 1024

LOG2_DB_SIZES = [10,12,14,16,18]

LOG2_ELEM_SIZES = [7, 9, 11, 13, 15]
ELEM_SIZES = [1<<i for i in LOG2_ELEM_SIZES]    # in bits

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

    os.chdir(SimplePirPath)
    results["simplepir"] = benchmark_SimplePir(log2_db_sizes, elem_sizes)
    results["simplepir_offline_include"] = benchmark_SimplePir(log2_db_sizes, elem_sizes, True)

    os.chdir(owd)
    os.chdir(SpiralPirPath)
    results["spiralpir"] = benchmark_SpiralPir(log2_db_sizes, elem_sizes)
    results["spiralpir_stream"] = benchmark_SpiralPir(log2_db_sizes, elem_sizes, True)

    os.chdir(owd)
    results["pirac"] = benchmark_pirac([1<<i for i in log2_db_sizes], 
                            [i//128 for i in elem_sizes], True, num_iter=5)
    
    return results

def gen_save_plot(results, x_values, x_label, fig_name):
    plt.figure()
    plt.yscale("log")

    plt.plot(x_values, results["simplepir"], "r-o", label="SimplePIR")
    plt.plot(x_values, results["simplepir_offline_include"], "r--o", label="SimplePIR (offline time included)")
    plt.plot(x_values, results["spiralpir"], "g-o", label="SpiralPIR")
    plt.plot(x_values, results["spiralpir_stream"], "g--o", label="SpiralPIR Stream")
    plt.plot(x_values, results["pirac"], "b-o", label="PIRAC")
    plt.xlabel(x_label)
    plt.ylabel("Throughput (in Mb/s)")
    plt.legend()
    plt.savefig(f"images/{fig_name}.png")
    print("Successfully generated and save the plot")

if __name__ == "__main__":
    args = parser.parse_args()
    exp_type = args.expType
    log2_db_sizes = args.dbSizes
    elem_sizes = args.elemSizes
    x_label = args.xLabel
    fig_name = args.figName
    
    if exp_type=="ds":
        log2_db_sizes = LOG2_DB_SIZES if log2_db_sizes is None else log2_db_sizes
        elem_sizes = [ELEM_SIZE] if elem_sizes is None else elem_sizes
        x_label = "Log2 of Number of Database entries" if x_label is None else x_label
        fig_name = "comparision_db_sizes" if fig_name is None else fig_name
        x_values = log2_db_sizes
    elif exp_type=="es":
        log2_db_sizes = [LOG2_DB_SIZE] if log2_db_sizes is None else log2_db_sizes
        elem_sizes = ELEM_SIZES if elem_sizes is None else elem_sizes
        x_label = "Log2 of Entry size (in bits)" if x_label is None else x_label
        fig_name = "comparision_elem_sizes" if fig_name is None else fig_name
        x_values = np.log2(elem_sizes)
    else:
        raise Exception("Shouldn't reach here")

    assert ((len(elem_sizes)==1) and (exp_type=="ds")) or \
            ((len(log2_db_sizes)==1) and (exp_type=="es"))
    
    results = run_PIRs(log2_db_sizes, elem_sizes)
    gen_save_plot(results, x_values, x_label, fig_name)
    
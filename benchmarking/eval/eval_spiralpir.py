import subprocess
import os
import json
import argparse
import numpy as np

from eval_pirac import benchmark_pirac

import utils

# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Run benchmarking for spiralpir')
parser.add_argument('-ds','--dbSizes', nargs='+',
                     required=False, type=int, default=utils.LOG2_DB_SIZES,
                     help='Log 2 Database sizes to run experiment on.')
parser.add_argument('-es','--elemSizes', nargs='+',
                     required=False, type=int, default=utils.ELEM_SIZES,
                     help='Element sizes (in bits) to run experiment on.')
parser.add_argument('-s','--stream', action='store_true',
                     required=False, 
                     help='If the flag is passed, run in streaming mode')
parser.add_argument('-p','--pack', action='store_true',
                     required=False, 
                     help='If the flag is passed, run in pack mode')
parser.add_argument('-o','--output', action='store_true',
                     required=False, 
                     help='If the flag is passed, display the output of the spiralpir')
parser.add_argument('-wp','--withPirac', choices=['re', 'pirac'],
                    required=False,
                    help='If passed "re", runs with reencryption. If passed with "pirac", run\
                        both rekeying and reencryption')

def run_SpiralPIR(N, D, stream=False, pack=False, output=False):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    # if "pack" in system:
    #     cmd += " --high-rate"
    stream_flag = "--direct-upload" if stream else ""
    pack_flag = " --high-rate" if pack else ""
    process = subprocess.Popen(f'python3 select_params.py {N} {D//8} {stream_flag} {pack_flag}', 
                            shell=True,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    statistics = None
    i = 0
    while True:
        line = process.stdout.readline()
        try:
            statistics = json.loads(line)
        except:
            pass # invalid parsing
        
        if output:
            print(i, line.rstrip())
            i+=1

        return_code = process.poll()
        if return_code is not None and output:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for line in process.stdout.readlines():
                print(line.strip())
            break
    
    assert statistics is not None
    return statistics["dbsize"]/statistics["total_us"]

def benchmark_SpiralPir(db_sizes, elem_sizes, stream=False, pack=False, output=False):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    throughputs = []
    for db_size in db_sizes:
        for elem_size in elem_sizes:
            throughput = run_SpiralPIR(db_size, elem_size, stream, pack, output)
            stream_print = "(with streaming)" if stream else ""
            pack_print = "(with pack)" if pack else ""
            print(f"Throughput on SpiralPIR {stream_print} {pack_print} with log2 dbsize = {db_size}, elem size = {elem_size} bits = {throughput}Mb/s")
            throughputs.append(throughput)
    
    return throughputs

def pretty_print(throughputs, stream, pack, pirac_mode):
    min_tput = np.min(throughputs)
    max_tput = np.max(throughputs)
    pp = f"Streaming = {stream}, Packing = {pack}, Pirac Mode = {pirac_mode}\n"
    pp = pp + "Throughputs in the range {0:0.1f}-{1:0.1f}Mb/s".format(min_tput, max_tput)
    print(pp)

if __name__ == "__main__":
    args = parser.parse_args()
    log2_db_sizes = args.dbSizes
    elem_sizes = args.elemSizes
    stream = args.stream
    pack = args.pack
    output = args.output
    pirac_mode = args.withPirac

    os.chdir(utils.SpiralPirPath)
    print(os.getcwd())

    throughputs_spiralpir = benchmark_SpiralPir(log2_db_sizes, elem_sizes, stream=stream, pack=pack, output=output)

    if pirac_mode is None:
        pretty_print(throughputs_spiralpir, stream, pack, pirac_mode)
    elif pirac_mode=="re":
        throughputs_re = benchmark_pirac(log2_db_sizes, elem_sizes,  10, rekeying = False)
        throughputs_combined = utils.cal_tput_with_pirac(throughputs_spiralpir, throughputs_re)
        pretty_print(throughputs_combined, stream, pack, pirac_mode)
    elif pirac_mode=="pirac":
        throughputs_pirac = benchmark_pirac(log2_db_sizes, elem_sizes,  10, rekeying = True)
        throughputs_combined = utils.cal_tput_with_pirac(throughputs_spiralpir, throughputs_pirac)
        pretty_print(throughputs_combined, stream, pack, pirac_mode)
    else:
        raise Exception("Shouldn't reach here")

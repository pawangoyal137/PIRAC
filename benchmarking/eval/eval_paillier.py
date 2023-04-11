import subprocess
import os
import re
import argparse
import numpy as np

from eval_pirac import benchmark_pirac
from utils import cal_tput_with_pirac, PaillierPath

# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Run benchmarking for paillier')
parser.add_argument('-o','--output', action='store_true',
                     required=False, 
                     help='If the flag is passed, display the output of the simplepir')
parser.add_argument('-wp','--withPirac', choices=['re', 'pirac'],
                    required=False,
                    help='If passed "re", runs with reencryption. If passed with "pirac", run\
                        both rekeying and reencryption')

BITS = 2048

def run_Paillier(output=False):
    test_name = "BenchmarkPaillierDifPrimes"
    process = subprocess.Popen(f"go test '-bench=^{test_name}$' '-run=^$'", 
                            shell=True,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    throughput = None
    if output:
        while True:
            output = process.stdout.readline()
            print(output.rstrip())
            if "Average throughput for paillier" in output:
                temp = re.findall(r'\d+\.?\d+', output)
                throughput = list(map(float, temp))
            return_code = process.poll()

            if return_code is not None:
                print('RETURN CODE', return_code)
                # Process has finished, read rest of the output 
                for output in process.stdout.readlines():
                    print(output.strip())
                break
    else:
        stdout, _ = process.communicate()
        for line in stdout.split('\n'):
            if "Average throughput for paillier" in line:
                temp = re.findall(r'\d+\.?\d+', line)
                throughput = list(map(float, temp))
                
    assert len(throughput)==1
    throughput = throughput[0]
    print(f"Throughput of Paillier = {throughput} MB/s")
    return throughput

def pretty_print(throughput, pirac_mode):
    pp = f"Running Paillier, Pirac Mode = {pirac_mode}\n"
    pp = pp + "Throughput: {0:0.4f} MB/s".format(throughput)
    print(pp)

if __name__ == "__main__":
    args = parser.parse_args()
    output = args.output
    pirac_mode = args.withPirac

    os.chdir(PaillierPath)

    throughput_paillier = run_Paillier(output=output)
    if pirac_mode is None:
        pretty_print(throughput_paillier, pirac_mode)
    elif pirac_mode=="re":
        throughputs_re = benchmark_pirac([16], [BITS],  10, rekeying = False)
        throughputs_combined = cal_tput_with_pirac([throughput_paillier], throughputs_re)
        pretty_print(throughputs_combined[0], pirac_mode)
    elif pirac_mode=="pirac":
        throughputs_pirac = benchmark_pirac([16], [BITS],  10, rekeying = True)
        throughputs_combined = cal_tput_with_pirac([throughput_paillier], throughputs_pirac)
        pretty_print(throughputs_combined[0], pirac_mode)
    else:
        raise Exception("Shouldn't reach here")

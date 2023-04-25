import subprocess
import os
import numpy as np

import utils

def cal_simplepir_tput(N, D, offline_include=False, output=False, num_iter=5):
    cwd = os.getcwd()
    os.chdir(utils.SimplePirPath)

    tputs = []
    for _ in range(max(num_iter//5,1)): #simple pir by default benchmark over 5 runs
        if offline_include:
            test_name = "BenchmarkSimplePirOfflineIncludeSingle"
        else:
            test_name = "BenchmarkSimplePirSingle"
        process = subprocess.Popen(f"LOG_N={N} D={D} go test '-bench=^{test_name}$' -timeout 0 '-run=^$'", 
                                shell=True,
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE,
                                universal_newlines=True)

        throughput = None
        while True:
            line = process.stdout.readline()
            if "Avg SimplePIR tput, except for first run" in line:
                throughput = utils.extract_num(line)
            
            if output:
                print(line.rstrip())

            return_code = process.poll()
            if return_code is not None:
                break
        
        if output:
            offline_print = "(with offline time)" if offline_include else ""
            print(f"Throughput on SimplePIR {offline_print} with log2 dbsize = {N}, elem size = {D} bits = {throughput}Mb/s")
        tputs.append(throughput)

    os.chdir(cwd)     
    return np.mean(tputs)

if __name__ == "__main__":
    pass

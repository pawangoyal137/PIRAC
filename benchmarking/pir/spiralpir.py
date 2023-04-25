import subprocess
import json
import os
import numpy as np

import utils

def cal_spiralpir_tput(N, D, stream=False, pack=False, output=False, num_iter=5):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    cwd = os.getcwd()
    os.chdir(utils.SpiralPirPath)

    stream_flag = "--direct-upload" if stream else ""
    pack_flag = " --high-rate" if pack else ""
    tputs = []

    for _ in range(num_iter):
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
            if return_code is not None:
                break
        
        assert statistics is not None
        tput = statistics["dbsize"]/statistics["total_us"]
        if output:
            stream_print = "(with streaming)" if stream else ""
            pack_print = "(with pack)" if pack else ""
            print(f"Throughput on SpiralPIR {stream_print} {pack_print} with log2 dbsize = {N}, elem size = {D} bits = {tput}MB/s")
        tputs.append(tput)

    os.chdir(cwd)
    return np.mean(tputs)

if __name__ == "__main__":
    pass


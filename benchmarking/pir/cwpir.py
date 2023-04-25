import subprocess
import os
import numpy as np

import utils

def cal_cwpir_tput(db_size, elem_size, kw, h, output=False, num_iter=5):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    cwd = os.getcwd()
    os.chdir(utils.CWPirPath)

    num_entries = (1<<db_size)
    elem_size_bytes = elem_size//8
    
    tputs = []
    for _ in range(num_iter):
        process = subprocess.Popen(f'./main -n {num_entries} -s {elem_size_bytes} -x {kw} -h {h} -d 13 -e 1 -t 1', 
                                shell=True,
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE,
                                universal_newlines=True)

        statistics = {}
        correct_response = False   
        i = 0
        while True:
            line = process.stdout.readline()
            if output:
                print(i, line.rstrip())
                i+=1
                
            if "Number of Keywords" in line:
                assert utils.extract_num(line)==num_entries
            elif "Keyword Max Bitlength" in line:
                assert utils.extract_num(line)==kw
            elif "Max Item Hex Length" in line:
                assert utils.extract_num(line)==elem_size_bytes*2
            elif "Hamming Weight" in line:
                assert utils.extract_num(line)==h
            elif "Correct Response!" in line:
                correct_response = True
            elif "Response Cipher Count" in line:
                statistics["num_output_ciphers"] = utils.extract_num(line)
            elif "Total Server" in line:
                statistics["total_ms"] = utils.extract_num(line)

            return_code = process.poll()
            if return_code is not None:
                break
        
        assert correct_response
        assert statistics is not None

        elem_size_mb =  ((2**13) * statistics["num_output_ciphers"] * 20 / 8000000)
        db_size_mb = num_entries * elem_size_mb
        throughput = 1000*db_size_mb/statistics["total_ms"]

        if output:
            print(f"Throughput on CWPIR  with kw = {kw}, Hamming weight = {h} \n\
                log2 dbsize = {db_size}, elem size = {elem_size} bits = {throughput}MB/s")
        tputs.append(throughput)

    os.chdir(cwd)
    return np.mean(tputs)


if __name__ == "__main__":
    pass

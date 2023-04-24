import subprocess
import re
import os

import utils

def cal_sealpir_tput(N, D, output=False):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    cwd = os.getcwd()
    os.chdir(utils.SealPirPath)

    maxsize = 24576 # 3072 bytes
    factor = utils.get_factor(D, maxsize)
    elem_size = min(maxsize, D)
    process = subprocess.Popen(f'./main {N} {elem_size//8}', 
                            shell=True,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    total_re = r"Main: PIRServer reply generation time.*:\s+([0-9]+)"
    exp_re = r"Server: Expansion time.*:\s+([0-9]+)"
    exp_us = 0
    i = 0
    while True:
        line = process.stdout.readline()
        try:
            total_us = int(re.search(total_re, line).group(1))*1000
        except:
            pass # invalid parsing

        try:
            exp_us += int(re.search(exp_re, line).group(1))
        except:
            pass # invalid parsing

        if output:
            print(i, line.rstrip())
            i+=1

        return_code = process.poll()
        if return_code is not None:
            break
    
    database_size_bytes = (1<<N)*(D//8)
    total_including_factor = (factor * (total_us-exp_us) + exp_us)
    if output:
        print(f"Total server time: {total_us} us, Expansion Time: {exp_us} us, Total Time after factor = {total_including_factor} us")
        print(f"Factor = {factor}, elem size = {elem_size}")
    
    os.chdir(cwd)
    return database_size_bytes/total_including_factor

if __name__ == "__main__":
    pass

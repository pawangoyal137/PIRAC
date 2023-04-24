import subprocess
import os

import utils

def cal_fastpir_tput(N, D, output=False):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    cwd = os.getcwd()
    os.chdir(utils.FastPirPath)

    maxsize = 72960 # 9120 bytes
    factor = utils.get_factor(D, maxsize)
    elem_size = min(maxsize, D)
    process = subprocess.Popen(f'bin/fastpir -n {1<<N} -s {elem_size//8}', 
                            shell=True,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    correct_result = False
    while True:
        line = process.stdout.readline()
        if "Response generation time" in line:
            total_us = utils.extract_num(line)
        if "PIR result correct!" in line:
            correct_result = True

        if output:
            print(line.rstrip())

        return_code = process.poll()
        if return_code is not None:
            break

    assert correct_result
    database_size_bytes = (1<<N)*(D//8)
    total_including_factor = factor * total_us

    if output:
        print(f"Factor = {factor}, elem size = {elem_size}")
        print(f"Total server time: {total_us} us, Total Time after factor = {total_including_factor} us")
    
    os.chdir(cwd)
    return database_size_bytes/total_including_factor

if __name__ == "__main__":
    pass

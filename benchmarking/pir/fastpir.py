import subprocess
import os
import numpy as np

import utils


def cal_fastpir_tput(N, D, output=False, num_iter=5):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    cwd = os.getcwd()
    os.chdir(utils.FastPirPath)

    maxsize = 72960  # 9120 bytes
    factor = utils.get_factor(D, maxsize)
    elem_size = min(maxsize, D)

    tputs = []
    for _ in range(num_iter):
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
        database_size_bytes = (1 << N)*(D//8)
        total_including_factor = factor * total_us

        tput = database_size_bytes/total_including_factor
        tputs.append(tput)

    if output:
        print(f"Factor = {factor}, elem size = {elem_size}")
        print(
            f"Total server time: {total_us} us, Total Time after factor = {total_including_factor} us")
        print(f"Throughput on Fastpir = {np.mean(tputs)}+-{np.std(tputs)}MB/s")
    os.chdir(cwd)
    return np.mean(tputs), np.std(tputs)


if __name__ == "__main__":
    pass

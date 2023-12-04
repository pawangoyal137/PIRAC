import subprocess
import os

import utils


def cal_paillier_tput(db_size, elem_size, output=False):
    cwd = os.getcwd()
    os.chdir(utils.PaillierPath)

    test_name = "BenchmarkPaillierDifPrimes"
    process = subprocess.Popen(f"go test '-bench=^{test_name}$' '-run=^$'",
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)

    tput = None
    tput_std = None
    while True:
        line = process.stdout.readline()
        if "Average throughput for paillier" in line:
            tput = utils.extract_num(line)
        if "Standard Deviation" in line:
            tput_std = utils.extract_num(line)
        if output:
            print(line.rstrip())

        return_code = process.poll()
        if return_code is not None:
            break

    if output:           
        print(f"Throughput of Paillier = {tput} +- {tput_std} MB/s")
    
    os.chdir(cwd)
    return tput, tput_std


if __name__ == "__main__":
    pass

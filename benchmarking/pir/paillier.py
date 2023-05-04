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

    throughput = None
    while True:
        line = process.stdout.readline()
        if "Average throughput for paillier" in line:
            throughput = utils.extract_num(line)

        if output:
            print(line.rstrip())

        return_code = process.poll()
        if return_code is not None:
            break

    if output:
        print(f"Throughput of Paillier = {throughput} MB/s")

    os.chdir(cwd)
    return throughput


if __name__ == "__main__":
    pass

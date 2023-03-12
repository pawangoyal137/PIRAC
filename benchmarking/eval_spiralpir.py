import subprocess
import os
import json

SpiralPirPath = "../../spiral"

def run_SpiralPIR(N, D, output=False):
    process = subprocess.Popen(f'python3 select_params.py {N} {D//8}', 
                            shell=True,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    statistics = None
    if output:
        i = 0
        while True:
            output = process.stdout.readline()
            print(i, output.strip())
            i+=1
            try:
                statistics = json.loads(output)
            except:
                pass # invalid parsing

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
            try:
                statistics = json.loads(line)
            except:
                pass # invalid parsing
    
    assert statistics is not None
    return statistics["dbsize"]/statistics["total_us"]

def benchmark_SpiralPir(db_sizes, elem_sizes):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    throughputs = []
    for db_size in db_sizes:
        for elem_size in elem_sizes:
            throughput = run_SpiralPIR(db_size, elem_size)
            print(f"Throughput on SpiralPIR with log2 dbsize = {db_size}, elem size = {elem_size} bits = {throughput}Mb/s")
            throughputs.append(throughput)
    
    return throughputs

if __name__ == "__main__":
    os.chdir(SpiralPirPath)
    print(os.getcwd())

    db_sizes = [10,12,14,16,18,20]
    elem_sizes = [1<<i for i in [7,9,11,13,15]] #in bits

    throughputs_dbsizes = benchmark_SpiralPir(db_sizes, [2048])
    # throughputs_elemsizes = benchmark_SimplePir(12, elem_sizes)

    print(throughputs_dbsizes)
    # print(throughputs_elemsizes)

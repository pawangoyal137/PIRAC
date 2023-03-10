import subprocess
import os
import re

SimplePirPath = "../simplepir/pir"

def run_SimplePIR(N, D, output=False):
    process = subprocess.Popen(f'LOG_N={N} D={D} go test -bench SimplePirSingle -timeout 0 -run="SimplePirSingle"', 
                            shell=True,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    throughput = None
    if output:
        while True:
            output = process.stdout.readline()
            print(output.strip())
            if "Avg SimplePIR tput, except for first run" in output:
                temp = re.findall(r'\d+\.?\d+', output)
                throughput = list(map(float, temp))
                assert len(throughput)==1
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
            if "Avg SimplePIR tput, except for first run" in line:
                temp = re.findall(r'\d+\.?\d+', line)
                throughput = list(map(float, temp))
                assert len(throughput)==1
    
    return throughput[0]

def benchmark_SimplePir(db_sizes, elem_sizes):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    throughputs = []
    for db_size in db_sizes:
        for elem_size in elem_sizes:
            throughput = run_SimplePIR(db_size, elem_size)
            print(f"Throughput on SimplePIR with log2 dbsize = {db_size}, elem size = {elem_size} bits = {throughput}Mb/s")
            throughputs.append(throughput)
    
    return throughputs

if __name__ == "__main__":
    os.chdir(SimplePirPath)
    print(os.getcwd())

    db_sizes = [10,12,14,16,18,20]
    elem_sizes = [1<<i for i in [7,9,11,13,15]] #in bits

    throughputs_dbsizes = benchmark_SimplePir(db_sizes, [2048])
    throughputs_elemsizes = benchmark_SimplePir(12, elem_sizes)

    print(throughputs_dbsizes)
    print(throughputs_elemsizes)

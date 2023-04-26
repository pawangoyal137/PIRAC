import json 
import utils 

from pirac import cal_pirac_tput


with open("results/data/fastpir.json") as f:
    # load JSON data as a list
    data_list = json.load(f)

final_results = []
for record in data_list:
    log2_db_size = record["log2_db_size"]
    elem_size = record["elem_size"]
    pir_tput = record["fastpir_bl_tput"]
    re_tput = cal_pirac_tput(log2_db_size, elem_size,  5, rekeying = False)
    pir_re_tput = utils.cal_tput_with_pirac(pir_tput, re_tput)
    record[f"fastpir_mp_tput"] = pir_re_tput
    record[f"fastpir_mp_overhead"] = pir_tput/pir_re_tput
    pirac_tput = cal_pirac_tput(log2_db_size, elem_size,  5, rekeying = True)
    pir_pirac_tput = utils.cal_tput_with_pirac(pir_tput, pirac_tput)
    record[f"fastpir_fs_tput"] = pir_pirac_tput
    record[f"fastpir_fs_overhead"] = pir_tput/ pir_pirac_tput
    final_results.append(record)    

with open("results/data/combined.json", "w") as outfile:
            json.dump(final_results, outfile, separators=(",\n", ": "))

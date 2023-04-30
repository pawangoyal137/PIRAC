OUTPUT_FOLDER=results/output_new
JSON_FILE_FOLDER=results/data/single_server_new
EVAL_FILE=pir/pir.py

pir_schemes=("simplepir" "spiralpir" "spiralstream" "spiralpack" "spiralstreampack" "sealpir" "fastpir")

for i in "${!pir_schemes[@]}"; do 
    OUTPUT_FILE="${OUTPUT_FOLDER}/${pir_schemes[i]}.txt"
    if test -f "$OUTPUT_FILE"; then
        truncate -s 0 "$OUTPUT_FILE"
    fi
    python3 "$EVAL_FILE" -n "${pir_schemes[i]}" -ds 20 -ni 5 -w "$JSON_FILE_FOLDER/${pir_schemes[i]}.json" -pm bl mp fs &>> "$OUTPUT_FILE"
    echo "-----------------------------------------------"
    echo "Final Results are as follows:"
    grep -E "^Range of|^Overhead of" "$OUTPUT_FILE" 
done



OUTPUT_FILE=results/output/spiralpir.txt
JSON_FILE_FOLDER=results/data
EVAL_FILE=bench-single-server/pir.py

if test -f "$OUTPUT_FILE"; then
    truncate -s 0 "$OUTPUT_FILE"
fi

# add_flags=('{}' '{"stream":"True"}' '{"pack":"True"}' '{"stream":"True", "pack":"True"}' )
pir_schemes=("spiralpir" "spiralstream" "spiralpack" "spiralstreampack")

for i in "${!pir_schemes[@]}"; do 
    python3 "$EVAL_FILE" -n "${pir_schemes[i]}" -w "$JSON_FILE_FOLDER/${pir_schemes[i]}.json" &>> "$OUTPUT_FILE"
    python3 "$EVAL_FILE" -n "${pir_schemes[i]}" -w "$JSON_FILE_FOLDER/${pir_schemes[i]}_re.json" -wp re &>> "$OUTPUT_FILE"
    python3 "$EVAL_FILE" -n "${pir_schemes[i]}" -w "$JSON_FILE_FOLDER/${pir_schemes[i]}_pirac.json" -wp pirac  &>> "$OUTPUT_FILE"
done

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^stream|^pack|^Pirac Mode|^Throughputs in the range" "$OUTPUT_FILE" 

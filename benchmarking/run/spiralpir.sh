OUTPUT_FILE=results/output/spiralpir.txt
JSON_FILE_FOLDER=results/data
EVAL_FILE=bench-single-server/pir.py

if test -f "$OUTPUT_FILE"; then
    truncate -s 0 "$OUTPUT_FILE"
fi

add_flags=('{}' '{"stream":"True"}' '{"pack":"True"}' '{"stream":"True", "pack":"True"}' )
pir_schemes=my_array=("spiralpir" "spiralstream" "spiralpack" "spiralstreampack")

for i in "${!my_array1[@]}"; do 
    python3 "$EVAL_FILE" -n spiralpir -w "$JSON_FILE_FOLDER/${my_array2[i]}.json" -arg="${my_array1[i]}" &>> "$OUTPUT_FILE"
    python3 "$EVAL_FILE" -n spiralpir -w "$JSON_FILE_FOLDER/${my_array2[i]}.json" -wp re  -arg="${my_array1[i]}" &>> "$OUTPUT_FILE"
    python3 "$EVAL_FILE" -n spiralpir -w "$JSON_FILE_FOLDER/${my_array2[i]}.json" -wp pirac  -arg="${my_array1[i]}" &>> "$OUTPUT_FILE"
done

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^stream|^pack|^Pirac Mode|^Throughputs in the range" "$OUTPUT_FILE" 

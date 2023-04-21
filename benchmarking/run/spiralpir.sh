OUTPUT_FILE=results/output/spiralpir.txt
JSON_FILE_FOLDER=results/data
EVAL_FILE=bench-single-server/pir.py

if test -f "$OUTPUT_FILE"; then
    truncate -s 0 "$OUTPUT_FILE"
fi

add_flags=('{}' '{"stream":"True"}' '{"pack":"True"}' '{"stream":"True", "pack":"True"}' )

for str in "${add_flags[@]}"
do  
    python3 "$EVAL_FILE" -n spiralpir -w "$JSON_FILE_FOLDER/spiralpir.json" -arg="$str" &>> "$OUTPUT_FILE"
    python3 "$EVAL_FILE" -n spiralpir -w "$JSON_FILE_FOLDER/spiralpir_re.json" -wp re  -arg="$str" &>> "$OUTPUT_FILE"
    python3 "$EVAL_FILE" -n spiralpir -w "$JSON_FILE_FOLDER/spiralpir_pirac.json" -wp pirac  -arg="$str" &>> "$OUTPUT_FILE"
done

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^stream|^pack|^Pirac Mode|^Throughputs in the range" "$OUTPUT_FILE" 
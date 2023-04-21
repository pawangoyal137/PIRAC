OUTPUT_FILE=results/output/simplepir.txt
JSON_FILE_FOLDER=results/data
EVAL_FILE=bench-single-server/pir.py

if test -f "$OUTPUT_FILE"; then
    truncate -s 0 "$OUTPUT_FILE"
fi

python3 "$EVAL_FILE" -n simplepir -w "$JSON_FILE_FOLDER/simplepir.json" &>> "$OUTPUT_FILE"
python3 "$EVAL_FILE" -n simplepir -w "$JSON_FILE_FOLDER/simplepir_re.json" -wp re  &>> "$OUTPUT_FILE"
python3 "$EVAL_FILE" -n simplepir -w "$JSON_FILE_FOLDER/simplepir_pirac.json" -wp pirac  &>> "$OUTPUT_FILE"

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Throughputs in the range" "$OUTPUT_FILE" 
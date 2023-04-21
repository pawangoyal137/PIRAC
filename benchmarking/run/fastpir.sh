OUTPUT_FILE=results/output/fastpir.txt
JSON_FILE_FOLDER=results/data
EVAL_FILE=bench-single-server/pir.py

if test -f "$OUTPUT_FILE"; then
    truncate -s 0 "$OUTPUT_FILE"
fi

python3 "$EVAL_FILE" -n fastpir -w "$JSON_FILE_FOLDER/fastpir.json" &>> "$OUTPUT_FILE"
python3 "$EVAL_FILE" -n fastpir -w "$JSON_FILE_FOLDER/fastpir_re.json" -wp re  &>> "$OUTPUT_FILE"
python3 "$EVAL_FILE" -n fastpir -w "$JSON_FILE_FOLDER/fastpir_pirac.json" -wp pirac  &>> "$OUTPUT_FILE"


echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Pirac Mode|^Throughputs in the range" "$OUTPUT_FILE" 
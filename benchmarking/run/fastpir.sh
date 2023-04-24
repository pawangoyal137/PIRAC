OUTPUT_FILE=results/output/fastpir.txt
JSON_FILE_FOLDER=results/data
EVAL_FILE=bench-single-server/pir.py

if test -f "$OUTPUT_FILE"; then
    truncate -s 0 "$OUTPUT_FILE"
fi

python3 "$EVAL_FILE" -n fastpir -w "$JSON_FILE_FOLDER/fastpir.json" -pm bl mp fs &>> "$OUTPUT_FILE"

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Range of" "$OUTPUT_FILE"  
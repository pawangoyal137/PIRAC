OUTPUT_FILE=results/output/cwpir.txt
JSON_FILE_FOLDER=results/data
EVAL_FILE=pir/pir.py

if test -f "$OUTPUT_FILE"; then
    truncate -s 0 "$OUTPUT_FILE"
fi

# Baseline
python3 "$EVAL_FILE" -n cwpir -w "$JSON_FILE_FOLDER/cwpir_baseline.json" -ds 10 -es 163840 327680 655360 1310720 2621440 -arg='{"h":2}' -o &>> "$OUTPUT_FILE"

# 48 bit keywords
# python3 "$EVAL_FILE" -n cwpir -w "$JSON_FILE_FOLDER/cwpir_48.json" -ds 10 -es 163840 327680 655360 1310720 2621440 -arg='{"kw:48", "h=5"}' -o &>> "$OUTPUT_FILE"

# for ((h=2; h<=8; h++)); do
#     python3 "$EVAL_FILE"  -ds 10 -es 163840 -hs $h -kw 48 -o &>> "$OUTPUT_FILE"
# done

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Range of|^Overhead of" "$OUTPUT_FILE" 
OUTPUT_FOLDER=results/output/
JSON_FILE_FOLDER=results/data
EVAL_FILE=pir/pir.py

# 48 bit keywords 
OUTPUT_FILE="${OUTPUT_FOLDER}/cwpir_48.txt"
if test -f "$OUTPUT_FILE"; then
    truncate -s 0 "$OUTPUT_FILE"
fi
python3 "$EVAL_FILE" -n cwpir -w "${JSON_FILE_FOLDER}/cwpir_48.json" -ds 10 -arg='{"kw":48, "h":5}' -o  &>> "$OUTPUT_FILE"
echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Range of|^Overhead of" "$OUTPUT_FILE" 

# Baseline
OUTPUT_FILE="${OUTPUT_FOLDER}/cwpir_baseline.txt"
if test -f "$OUTPUT_FILE"; then
    truncate -s 0 "$OUTPUT_FILE"
fi
python3 "$EVAL_FILE" -n cwpir -w "$JSON_FILE_FOLDER/cwpir_baseline.json" -ds 10 -arg='{"h":2}' -o &>> "$OUTPUT_FILE"
echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Range of|^Overhead of" "$OUTPUT_FILE" 

# 128 512 2048 8192 32768
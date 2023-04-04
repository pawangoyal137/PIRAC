OUTPUT_FILE=outputs/spiralpir.txt
EVAL_FILE=eval/eval_spiralpir.py

if test -f "$OUTPUT_FILE"; then
    truncate -s 0 "$OUTPUT_FILE"
fi

python3 "$EVAL_FILE" &>> "$OUTPUT_FILE"
python3 "$EVAL_FILE" -wp re  &>> "$OUTPUT_FILE"
python3 "$EVAL_FILE" -wp pirac  &>> "$OUTPUT_FILE"

python3 "$EVAL_FILE" -s &>> "$OUTPUT_FILE"
python3 "$EVAL_FILE" -wp re -s  &>> "$OUTPUT_FILE"
python3 "$EVAL_FILE" -wp pirac -s  &>> "$OUTPUT_FILE"

python3 "$EVAL_FILE" -p &>> "$OUTPUT_FILE"
python3 "$EVAL_FILE" -wp re -p &>> "$OUTPUT_FILE"
python3 "$EVAL_FILE" -wp pirac -p &>> "$OUTPUT_FILE"

python3 "$EVAL_FILE" -s -p &>> "$OUTPUT_FILE"
python3 "$EVAL_FILE" -wp re -s -p &>> "$OUTPUT_FILE"
python3 "$EVAL_FILE" -wp pirac -s -p &>> "$OUTPUT_FILE"

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Streaming|^Throughputs in the range" "$OUTPUT_FILE" 
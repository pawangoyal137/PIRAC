OUTPUT_FILE=outputs/fastpir.txt
EVAL_FILE=eval/eval_fastpir.py

if test -f "$OUTPUT_FILE"; then
    truncate -s 0 "$OUTPUT_FILE"
fi

python3 $EVAL_FILE &>> "$OUTPUT_FILE"
python3 $EVAL_FILE -wp re  &>> "$OUTPUT_FILE"
python3 $EVAL_FILE -wp pirac  &>> "$OUTPUT_FILE"

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Pirac Mode|^Throughputs in the range" "$OUTPUT_FILE" 
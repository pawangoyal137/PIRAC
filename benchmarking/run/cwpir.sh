OUTPUT_FILE=outputs/cwpir.txt
EVAL_FILE=eval/eval_cwpir.py

if test -f "$OUTPUT_FILE"; then
    truncate -s 0 "$OUTPUT_FILE"
fi

for ((i=0; i<=4; i++)); do
    python3 "$EVAL_FILE"  -ds 10 -es $((163840 * 2**i)) -hs 5 -kw 48 -o &>> "$OUTPUT_FILE"
done

# for ((h=2; h<=8; h++)); do
#     python3 "$EVAL_FILE"  -ds 10 -es 163840 -hs $h -kw 48 -o &>> "$OUTPUT_FILE"
# done

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Throughput on CWPIR|^\s*log2 db" "$OUTPUT_FILE" 
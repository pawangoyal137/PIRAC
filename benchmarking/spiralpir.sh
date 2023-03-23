FILE=outputs/spiralpir.txt
if test -f "$FILE"; then
    truncate -s 0 "$FILE"
fi

python3 eval_spiralpir.py -ds 16 -es 1024 &>> "$FILE"
python3 eval_spiralpir.py -ds 16 -es 1024 -s &>> "$FILE"

# python3 eval_spiralpir.py -wp re  &>> "$FILE"
# python3 eval_spiralpir.py -wp re -s  &>> "$FILE"

# python3 eval_spiralpir.py -wp pirac  &>> "$FILE"
# python3 eval_spiralpir.py -wp pirac -s  &>> "$FILE"

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Streaming|^Throughputs in the range" "$FILE" 
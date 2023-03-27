FILE=outputs/sealpir.txt
if test -f "$FILE"; then
    truncate -s 0 "$FILE"
fi

python3 eval_sealpir.py &>> "$FILE"
python3 eval_sealpir.py -wp re  &>> "$FILE"
python3 eval_sealpir.py -wp pirac  &>> "$FILE"

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Pirac Mode|^Throughputs in the range" "$FILE" 
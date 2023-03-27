FILE=outputs/spiralpir.txt
if test -f "$FILE"; then
    truncate -s 0 "$FILE"
fi

python3 eval_spiralpir.py &>> "$FILE"
python3 eval_spiralpir.py -wp re  &>> "$FILE"
python3 eval_spiralpir.py -wp pirac  &>> "$FILE"

python3 eval_spiralpir.py -s &>> "$FILE"
python3 eval_spiralpir.py -wp re -s  &>> "$FILE"
python3 eval_spiralpir.py -wp pirac -s  &>> "$FILE"

python3 eval_spiralpir.py -p &>> "$FILE"
python3 eval_spiralpir.py -wp re -p &>> "$FILE"
python3 eval_spiralpir.py -wp pirac -p &>> "$FILE"

python3 eval_spiralpir.py -s -p &>> "$FILE"
python3 eval_spiralpir.py -wp re -s -p &>> "$FILE"
python3 eval_spiralpir.py -wp pirac -s -p &>> "$FILE"

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Streaming|^Throughputs in the range" "$FILE" 
FILE=outputs/simplepir.txt
if test -f "$FILE"; then
    truncate -s 0 "$FILE"
fi

python3 eval_simplepir.py &>> "$FILE"
python3 eval_simplepir.py -o &>> "$FILE"

python3 eval_simplepir.py -wp re  &>> "$FILE"
python3 eval_simplepir.py -wp re -o  &>> "$FILE"

python3 eval_simplepir.py -wp pirac  &>> "$FILE"
python3 eval_simplepir.py -wp pirac -o  &>> "$FILE"

echo "-----------------------------------------------"
echo "Final Results are as follows:"
grep -E "^Offline Mode|^Throughputs in the range" "$FILE" 
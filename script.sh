#!/bin/bash
for (( ; ; ))
do
    cat valor.txt | xargs ./text2pixels.py > displayLCD.txt
    sed 's/ /0/g' displayLCD.txt | paste -sd "" - > arquivofinal.txt
    sleep 1
done

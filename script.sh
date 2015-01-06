#!/bin/bash
for (( ; ; ))
do
    cat valor.txt | xargs ./text2pixels.py -m | paste -sd "" - > arquivofinal.txt
    sleep 1
done

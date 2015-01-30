#!/usr/bin/env python

import json
import requests
import time
import random
import sys

import locale


x = 1
while True: 
    
    valor_exibicao = ",,,," + str(random.randrange(0,8+1)) + str(random.randrange(0,8+1)) + str(random.randrange(0,8+1)) + str(random.randrange(0,8+1))
    print (valor_exibicao)
    text_file = open("valor.txt", "w")
    text_file.write(valor_exibicao)
    text_file.close()

    time.sleep(1)

    x +=1

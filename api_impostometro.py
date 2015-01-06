# -*- coding: utf-8 -*-

import text2pixels
import json
import requests
import time
import random
import sys

import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

x = 1
while True: 
    
    r = requests.get('http://api.impostometro.com.br/services/brasil')
    if r.status_code == 200:
        impostometro_dados = json.loads(r.content)



    a = float(impostometro_dados['atual'])
    seg = float(impostometro_dados['segundo'])
    valorFinal = a + seg + random.randrange(0,8+1)/10 + random.randrange(0,8+1)/100
    print (str(a) + "  <---  valor atual online")
    print (str(seg) + "  <---incremento por segundo atual online")
    yy = locale.format("%10.2f", valorFinal, grouping=True)
    print (yy)

    for i in range(10):
   
        print(locale.format("%10.2f", valorFinal, grouping=True))
        valorFinal = valorFinal + seg + random.randrange(0,8+1)/10 + random.randrange(0,8+1)/100    
        time.sleep(1)

    x +=1

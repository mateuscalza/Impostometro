#!/usr/bin/env python

import text2pixels
import json
import requests
import time
import random
import sys

import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

impostometro_dados_antigo = {u'atual':123456789,u'segundo':456789}

x = 1
while True: 
    try:
        r = requests.get('http://api.impostometro.com.br/services/brasil', timeout=5)
        impostometro_dados = json.loads(r.content) 

    except: 
        impostometro_dados = impostometro_dados_antigo

    a = float(impostometro_dados['atual'])
    seg = float(impostometro_dados['segundo'])
    valorFinal = a + seg + random.randrange(0,8+1)/10 + random.randrange(0,8+1)/100
    print (str(a) + "  <---  valor atual online")
    print (str(seg) + "  <---incremento por segundo atual online")

    for i in range(5):
        valor_exibicao = locale.format("%016.2f", valorFinal, grouping=True)
        print(valor_exibicao)
        #valorFinal = valorFinal + seg + random.randrange(0,8+1)/10 + random.randrange(0,8+1)/100
        valorFinal = valorFinal + seg + random.randrange(0,8+1)*1000000000 + random.randrange(0,8+1)*10000000000    

        text_file = open("valor.txt", "w")
        text_file.write(valor_exibicao)
        text_file.close()

        time.sleep(1)

    impostometro_dados_antigo = impostometro_dados
    print (impostometro_dados_antigo)
    x +=1

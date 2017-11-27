#!/usr/bin/env python

# -*- coding: utf-8 -*-

import text2pixels
import json
import requests
import time
import random
import sys
import locale

from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

dia = 0
valor_final = 0
incremento_por_segundo = 94747.37
while True:
    agora = datetime.now()
    hoje = agora.day
    if dia != hoje or valor_final == 0:
        dia = hoje
        mes = agora.month
        ano = agora.year
        try:
            headers = {'X-Requested-With': 'XMLHttpRequest'}
            url = 'https://impostometro.com.br/Contador/Brasil?dataInicial=01/01/' + str(ano) + '&dataFinal=' + str(dia) + '/' + str(mes) + '/' + str(ano)
            print(url)
            r = requests.get(url, headers=headers, timeout=10, verify=False)
            if r.status_code == 200:
	        impostometro_dados = json.loads(r.content)
	        valor_final = float(impostometro_dados['Valor'])
                print(str(valor_final) + ' (novo valor da API)')
            else:
                print("Ocorreu um erro, resposta:")
                print(r.content)
        except:
            print("Ocorreu um erro")

    if valor_final == 0:
        valor_exibicao = "."
        print("Ocorreu um erro, sem valor para exibir.")
    else:
        valor_final += incremento_por_segundo
        valor_exibicao = locale.format("%016.2f", valor_final, grouping=True)
        print(valor_exibicao)

        text_file = open("valor.txt", "w")
        text_file.write(valor_exibicao)
        text_file.close()
    time.sleep(1)

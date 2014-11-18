# -*- coding: utf-8 -*-

import json
import requests
import time
import random
print "Calculando Impostos de 01/01/2014 até " + time.strftime('%d/%d/%y %H:%M:%S')


x = 1
while True:
    r = requests.get('http://api.impostometro.com.br/services/brasil')
    if r.status_code == 200:
        impostometro_dados = json.loads(r.content)

    a = impostometro_dados['atual']
    b = format(int(a), ',d')
    centavo1 = str(random.randrange(0,8+1))
    centavo2 = str(random.randrange(0,8+1))
    print b.replace(',', '.') + ',' + centavo1 + centavo2
    x += 1

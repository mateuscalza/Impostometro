#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime
import requests
import json
import time
import random

lcd = Adafruit_CharLCD()

lcd.begin(16, 1)

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output


while 1:

    r = requests.get('http://api.impostometro.com.br/services/brasil')
    if r.status_code == 200:
        impostometro_dados = json.loads(r.content)
    a = impostometro_dados['atual']
    b = format(int(a), ',d')
      
#    lcd.clear()
    lcd.message('Impostometro\n')
    lcd.message(b)
    sleep(0)

#x = 1
#while True:

#    centavo1 = str(random.randrange(0,8+1))
#    centavo2 = str(random.randrange(0,8+1))
#    print b.replace(',', '.') + ',' + centavo1 + centavo2
#    x += 1


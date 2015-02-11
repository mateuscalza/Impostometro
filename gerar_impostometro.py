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

FONTE_VIR="x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,y,y,y,y,x,x,x,y,y,y,y,x,x,x,y,y,y,x,x,x,y,y,y,y,x,x,x,y,y,y,x,x,x,x,y,y,y,x,x,x,x,y,y,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,x,"
FONTE_PON="x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,y,y,y,y,x,x,x,y,y,y,y,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,"
FONTE_0="x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,x,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,x,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,"
FONTE_1="x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,"
FONTE_2="x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x"
FONTE_3="x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x"
FONTE_4="x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x"
FONTE_5="x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x"
FONTE_6="x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,y,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,y,y,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,y,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,x,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x"
FONTE_7="x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x"
FONTE_8="x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,x,y,y,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,y,y,y,y,y,y,y,y,x,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x"
FONTE_9="x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,x,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,y,x,x,x,x,x,x,y,y,y,y,y,y,x,x,x,x,y,y,y,y,y,y,y,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,x,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,x,x,y,y,y,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,x,x,x,x,x,x,x,x,y,y,x,x,x,x,x,x,x,x,y,y,y,y,y,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,y,y,y,y,y,y,y,y,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,y,y,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x"



x = 1
while True:
	start_update = time.time()
	try:
		r = requests.get('http://api.impostometro.com.br/services/brasil', timeout=5)
		impostometro_dados = json.loads(r.content)
		
	except:
		impostometro_dados = impostometro_dados_antigo
		print "Falha ao baixar valores atualizados"
	end_update = time.time()	
	print "Dados atualizados com sucesso! (%.4f segundos)" % (end_update - start_update)
	a = float(impostometro_dados['atual'])
	seg = float(impostometro_dados['segundo'])
	valorFinal = a + seg + random.randrange(0,8+1)/10 + random.randrange(0,8+1)/100

	for i in range(10):
		antes = time.time()
		valor_exibicao = locale.format("%016.2f", valorFinal, grouping=True)
		valorFinal = valorFinal + seg + random.randrange(0,8+1)/10 + random.randrange(0,8+1)/100
		valor = str(valor_exibicao)
		print str(valor_exibicao)
		linha = ""
		linha2 = ""    
		
		for i in range(0,16):
			iter1 = valor.replace(",",FONTE_VIR[i*14:i*14+14])
			iter2 = iter1.replace(".",FONTE_PON[i*14:i*14+14])
			iter3 = iter2.replace("0",FONTE_0[i*46:i*46+46])
			iter4 = iter3.replace("1",FONTE_1[i*46:i*46+46])
			iter5 = iter4.replace("2",FONTE_2[i*46:i*46+46])
			iter6 = iter5.replace("3",FONTE_3[i*46:i*46+46])
			iter7 = iter6.replace("4",FONTE_4[i*46:i*46+46])
			iter8 = iter7.replace("5",FONTE_5[i*46:i*46+46])
			iter9 = iter8.replace("6",FONTE_6[i*46:i*46+46])
			iter10 = iter9.replace("7",FONTE_7[i*46:i*46+46])
			iter11 = iter10.replace("8",FONTE_8[i*46:i*46+46])
			iterF = iter11.replace("9",FONTE_9[i*46:i*46+46])
			linha += iterF + "x,x,x,x," + "\n"

		for i in range(16,32):
			iter1 = valor.replace(",",FONTE_VIR[i*14:i*14+14])
			iter2 = iter1.replace(".",FONTE_PON[i*14:i*14+14])
			iter3 = iter2.replace("0",FONTE_0[i*46:i*46+46])
			iter4 = iter3.replace("1",FONTE_1[i*46:i*46+46])
			iter5 = iter4.replace("2",FONTE_2[i*46:i*46+46])
			iter6 = iter5.replace("3",FONTE_3[i*46:i*46+46])
			iter7 = iter6.replace("4",FONTE_4[i*46:i*46+46])
			iter8 = iter7.replace("5",FONTE_5[i*46:i*46+46])
			iter9 = iter8.replace("6",FONTE_6[i*46:i*46+46])
			iter10 = iter9.replace("7",FONTE_7[i*46:i*46+46])
			iter11 = iter10.replace("8",FONTE_8[i*46:i*46+46])
			iterF = iter11.replace("9",FONTE_9[i*46:i*46+46])
			linha2 += iterF + "x,x,x,x," + "\n"
		
		linhaF = linha + linha2[::-1]
       
		verFinal1 = linhaF.replace("x","0")
		verFinal2 = verFinal1.replace("y","1")
		verFinal3 = verFinal2.replace('00','0,0')
		verFinal4 = verFinal3.replace(',,',',')
		verFinal5 = verFinal4.replace('\n','')
		verFinal6 = verFinal5.replace(',,',',')

		f = open('arquivo.txt','w')
		f.write(verFinal6)
		f.close()


		parada = time.time()-antes
		time.sleep(1-parada)
		impostometro_dados_antigo = impostometro_dados
		x +=1
		print "Demorou %.4f segundos para todo o processo" % parada

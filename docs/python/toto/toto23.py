#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random

ileliczb = raw_input("Podaj ilość typowanych liczb: ")
zakres = raw_input("Podaj zakres losowanych liczb: ")
#print "Wytypuj",ileliczb,"z",zakres," liczb: "

liczby = []
i = 0
while i < int(ileliczb):
    liczba = random.randint(1, int(zakres))
    if liczby.count(liczba) == 0:
        liczby.append(liczba)
        i = i + 1

#print "Wylosowane liczby:",liczby

print "Wytypuj",ileliczb,"z",zakres," liczb: "
typy = set()
i = 0
while i < int(ileliczb):
    typ = raw_input("Podaj liczbę "+str(i+1)+": ")
    if typ not in typy:
        typy.add(typ)
        i = i + 1

print "Wytypowane liczby:",typy

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

os.chdir('../')
sys.path.append('saveload')

import bge
import saveload as sl

test = sl.SaveLoad()

#Récupérer tous les profils
datas = test.get_profil(None)
print(datas)

print('***********************')

#Normalement la variable bge.logic.globalDict['currentuser'] est défini au lancement du jeu lors de la sélection de profil....
bge.logic.globalDict['currentuser'] = 'default'

#Rcupérer un profil défini
datas = test.get_profil(bge.logic.globalDict['currentuser'])
print(datas)

print('***********************')

#Mettre à jour les infos d'un profil donné...
tmp = {"armure": 1, "belier": 2, "miniturbo": 1, "catapulte": 0, "decollage": 4, "lames": 0, "pistocell": 0, "mitraillette": 6}
#datas = test.set_profil(bge.logic.globalDict['currentuser'], tmp)
#print('Retour: ' + str(datas))


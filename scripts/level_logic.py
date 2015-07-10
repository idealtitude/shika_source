#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

os.chdir('../')
sys.path.append('saveload')

import bge
import saveload as sl

saveload = sl.SaveLoad()

scene = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()
own = cont.owner

sound_start = cont.actuators['sound_start']


player = scene.objects['player']
player_logic = player.groupMembers['player']

delay_intro = 3     #durée de l'animation d'intro et du compte à rebours



def init():

    print("initialisation du niveau")

    #Normalement la variable bge.logic.globalDict['currentuser'] est définie au lancement du jeu lors de la sélection de profil....
    bge.logic.globalDict['currentuser'] = 'default'
    #charger le profil
    profilDatas = saveload.get_profil(bge.logic.globalDict['currentuser'])
    
    #bloquer les contrôles du kart
    player_logic['active'] = False

    #Liste checkpoints
    listcheckpointobj = []
    #ajout checkpoints existants
    for i in scene.objects:
        prop = i.get("checkpoint", None)
        if prop is not None:
            listcheckpointobj.append(i)
    print(listcheckpointobj)
    
    
def main():
    if not 'started' in own:
        myTime = own['intro_delay'] - own['intro_timer']
        if myTime <= 0:
            own['started']=True
            player_logic['active'] = True
            cont.activate(sound_start)
            own['race_timer'] = 0

    

if 'init' not in own:
    own['init']=True
    init()

main() 

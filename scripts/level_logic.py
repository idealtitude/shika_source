#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

os.chdir('../')
sys.path.append('saveload')

import bge
#import saveload as sl
#saveload = sl.SaveLoad()

scene = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()
own = cont.owner

#récupérer les actuators
sound_start = cont.actuators['sound_start']

#récupérer les sensors
passCheckpoint = cont.sensors["passCheckpoint"]



def init():
        
    #récupérer le joueur et s'y attacher
    if 'player' in scene.objects:
        own['player'] = scene.objects['player']
        own['player_logic'] = own['player'].groupMembers['player']
    else:
        print("Impossible de trouver l'objet 'player' dans la scène")


    #définir les animations de Maskito
    if 'maskito' in scene.objects:
        own['maskito'] = scene.objects['maskito'].groupMembers['Armature']
        own['maskitoActions'] = {                          # 'action' : ('nom', durée)
            'getIn' : ('maskitoGetIn', 100),        # arrivée du perso
            'giveStart' : ('maskitoGiveStart', 50), # compte à rebours
            'getOut' :('maskitoGetOut', 60)         # départ du perso
            }
    else:
        print("Impossible de trouver l'objet 'maskito' dans la scène")


        
    
    #Normalement la variable bge.logic.globalDict['currentuser'] est définie au lancement du jeu lors de la sélection de profil....
    #bge.logic.globalDict['currentuser'] = 'default'
    #charger le profil
    #profilDatas = saveload.get_profil(bge.logic.globalDict['currentuser'])
    

    if 'player_logic' in own:
        #bloquer les contrôles du kart
        own['player_logic']['active'] = False

        #se parenter au kart
        own.worldPosition = own['player_logic'].worldPosition
        own.setParent(own['player_logic'],False,False)


    #Liste checkpoints
    checkpoints = []
    #détecter les checkpoints dans la scène
    for i in scene.objects:
        prop = i.get("checkpoint", None)
        if 'order' in i:
            newCheckpoint = (i, i['order'])
            checkpoints.append(newCheckpoint)
    #trier les checkpoints (selon la valeur de leur proriété 'order')
    checkpoints = (sorted(checkpoints, key=lambda cp: cp[1]))
    own['checkpoints'] = checkpoints
    own['passedCheckpoints'] = []
       
    
    if 'maskito' in own:
        #lancer l'animation de l'arrivée de Maskito    
        own['maskito'].playAction(own['maskitoActions']['getIn'][0], 1,own['maskitoActions']['getIn'][1], layer=1, play_mode=0)


def main():

    if not 'raceStarted' in own:
        if 'maskito' in own:
            #maskito est présent dans la scene, on attend qu'il ait donné le départ pour commencer la course
            #si maskito a fini son animation d'arrivée, il lance le décompte
            if own['maskito'].getActionFrame(1) >= own['maskitoActions']['getIn'][1]:
                own['maskito'].playAction(own['maskitoActions']['giveStart'][0], 1,own['maskitoActions']['giveStart'][1], layer=2, play_mode=0)
            #si maskito a fini le décompte, il donne le signale de départ et la course commence
            if own['maskito'].getActionFrame(2) >= own['maskitoActions']['giveStart'][1]:
                own['maskito'].playAction(own['maskitoActions']['getOut'][0], 1,own['maskitoActions']['getOut'][1], layer=3, play_mode=0)
                cont.activate(sound_start)
                
                own['raceStarted']=True
                own['race_timer'] = 0
                if 'player_logic' in own:                
                    own['player_logic']['active'] = True

        else:
            #maskito n'est pas dans la scene, la course commence directement
                own['raceStarted']=True
                own['race_timer'] = 0
                if 'player_logic' in own:
                    own['player_logic']['active'] = True


        
    if passCheckpoint.positive:
        justPassedCheckpoint = passCheckpoint.hitObject.groupObject
        # si on vient de passer le bon checkpoint (= le premier dans la liste)
        if (len(own['checkpoints']) > 0) and (str(own['checkpoints'][0][0]) == str(justPassedCheckpoint.name)):
            # ajouter le checkpoint à la liste de ceux validés
            own['passedCheckpoints'] += own['checkpoints'][0]
            # le retirer de la liste principale
            own['checkpoints'].pop(0)

    if 'checkpoints' in own:
        if (not 'raceFinished' in own) and (len(own['checkpoints']) == 0):
            print("Tous les checkpoints ont été passés dans l'ordre, la course est terminée.")
            print("Votre temps : %s" % own['race_timer'])
            own['raceFinished']=True


    if ('raceFinished' in own) and ('player_logic' in own):
        #bloquer les contrôles du kart. Pourquoi ça ne fonctionne pas ???
        own['player_logic']['active'] = False

if 'init' not in own:
    own['init']=True
    init()

main() 

import sys
import os
import json

import aud

import bpy

# So we can find the bgui module
sys.path.append('../..')

import bgui
import bgui.bge_utils
import bge

from saveload import saveload #Import du module saveload

getusers = saveload.UsersMng() #Instanciation de la classe UsersMng
bge.logic.globalDict['users'] = getusers.read_table(0) #On récupère toutes les entrées de la table users et on colle le tout dans le gloabldict `users`

MENU_CLICK = bpy.path.abspath("//") + 'audio' + os.sep + 'menu_click.mp3'


class MenuMain(bgui.bge_utils.Layout):

    def __init__(self, sys, data):
        super().__init__(sys, data)

        posx = 0.03
        posy = 0.700
        checkx = 1
        button = None
        strbut = ''
        lblist = []

        #Beep click menu
        self.soundclick = aud.Factory.file(MENU_CLICK)
        self.device = aud.device()

        for item in bge.logic.globalDict['users']:
            strbut = item
            lblist.append(strbut)
            button = bgui.FrameButton(self, text=strbut, size=[.16, .09], pos=[posx, posy], options = bgui.BGUI_DEFAULT)
            button.on_click = self.onBut
            posx += 0.20
            checkx += 1
            if checkx == 4:
                posy -= 0.100
                posx = 0.03
                checkx = 1

        #self.lb = bgui.ListBox(self, "lb", items=lblist, padding=0.05, size=[0.9, 0.9], pos=[0.05, 0.05])

        self.buttonAddProfil = bgui.FrameButton(self, text="Nouveau", size=[.18, .09], pos=[0.22, 0.05], options = bgui.BGUI_DEFAULT)
        self.buttonAddProfil.on_click = self.onAdd

        self.buttonexit = bgui.FrameButton(self, text="Quitter", size=[.18, .09], pos=[.03, 0.05], options = bgui.BGUI_DEFAULT)
        self.buttonexit.on_click = self.onExit

    def onBut(self, widget):
        self.device.play(self.soundclick)
        scene = bge.logic.addScene('loading')
        tmp = bge.logic.globalDict['users'][widget.text]
        bge.logic.globalDict['current_profil'] = widget.text
        bge.logic.globalDict['user_profil'] = tmp
        blendfile = bpy.path.abspath("//") + os.sep + 'main_menu.blend'
        bge.logic.startGame(blendfile)

    def onAdd(self, widget):
        blendfile = bpy.path.abspath("//") + os.sep + 'add_user.blend'
        bge.logic.startGame(blendfile)
        self.device.play(self.soundclick)

    def onExit(self, widget):
        #sys.exit() Ferme blender...
        self.device.play(self.soundclick)
        bge.logic.endGame()


def main(cont):
    own = cont.owner
    mouse = bge.logic.mouse

    if 'sys' not in own:
        # Create our system and show the mouse
        own['sys'] = bgui.bge_utils.System('themes/default')
        own['sys'].load_layout(MenuMain, None)
        mouse.visible = True
    else:
        own['sys'].run()

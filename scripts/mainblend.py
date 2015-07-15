import sys
import os
import json

import bge


REAL_CWD = os.getcwd()
CONFIG_FILE = REAL_CWD + os.sep + 'scripts' + os.sep + 'config.json'
MAIN_MENU = REAL_CWD + os.sep + 'main_menu.blend'
PROFIL_SELECT = REAL_CWD + os.sep + 'profil_select.blend'


class ShikaGame:
    def __init__(self):
        check = True
        try:
            f = open(CONFIG_FILE, 'r')
        except IOError:
            check = False
            print('Fichier de configuration introuvable à l\'emplacement attendu! Game exit...')
            bge.logic.endGame()

        if check:
            self.datas = None
            self._get_config()
            self._routage()

    def _get_config(self):
        with open(CONFIG_FILE) as data_source:
            self.datas = json.load(data_source)

    def _routage(self):
        if self.datas['user_prefs']['load_profil_on_launch'] == 1:
            bge.logic.globalDict['curent_profil'] = self.datas['user_prefs']['current_profil']] 
            bge.logic.startGame(MAIN_MENU)
        else:
            bge.logic.startGame(PROFIL_SELECT)


def main():
    launch_game = ShikaGame()


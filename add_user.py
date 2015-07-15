import sys
import os
import random

#import unicodedata
#import string

# So we can find the bgui module
sys.path.append('../..')

import bpy
import bgui
import bgui.bge_utils
import bge

from saveload import saveload #Import du module saveload

REAL_CWD = os.getcwd()

class SimpleLayout(bgui.bge_utils.Layout):
    """A layout showcasing various Bgui features"""

    def __init__(self, sys, data):
        super().__init__(sys, data)

        self.profil_name = bgui.TextInput(self, text="Nom de la sauvegarde", size=[.4, .04], pos=[.04, 0.08], input_options = bgui.BGUI_INPUT_NONE, options = bgui.BGUI_DEFAULT)

        self.profil_name.on_enter_key = self.on_input_enter
        
    def on_input_enter(self, widget):
        newname = widget.text
        widget.deactivate()
        
        if len(newname) > 0:
            #Nettoyage nom
            allowed_chars = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            newname = newname[0:20]
            tmpname = ''
            for i in newname:
                if i in allowed_chars:
                    tmpname = tmpname + i
                    
            newname = tmpname
                    
            #newname = ''.join(x for x in unicodedata.normalize('NFKD', newname) if x in string.ascii_letters).lower()
            
            #Key authentification HOF
            key = ''.join(random.choice(allowed_chars) for _ in range(32))
        
            #Assignation globaldict
            newprofil = {"iduser": "", "name": newname, "argent": 100, "courses": "0 0 0", "achievements": "0 0 0", "date": "", "key": key}
            bge.logic.globalDict['current_profil'] = newname
            bge.logic.globalDict['user_profil'] = newprofil
            
            #Insert dans la table users
            adduser = saveload.UsersMng()
            save = adduser.add_user(newprofil)
            
            bge.logic.globalDict['user_profil']['iduser'] = save
            
            blendfile = REAL_CWD + os.sep + 'main_menu.blend'
            bge.logic.startGame(blendfile)


def main(cont):
    own = cont.owner
    mouse = bge.logic.mouse

    if 'sys' not in own:
        # Create our system and show the mouse
        own['sys'] = bgui.bge_utils.System('../../themes/default')
        own['sys'].load_layout(SimpleLayout, None)
        mouse.visible = True
    else:
        own['sys'].run()

import sys
import os
import aud

# So we can find the bgui module
sys.path.append('../..')

import bgui
import bgui.bge_utils
import bge

from saveload import saveload #Import du module saveload

#Get datas (autres tables)
usracc = saveload.UsersDatas()
bge.logic.globalDict['accessoires'] = usracc.get_user_datas(bge.logic.globalDict['user_profil']['iduser'], 'accessoires')
bge.logic.globalDict['preferences'] = usracc.get_user_datas(bge.logic.globalDict['user_profil']['iduser'], 'preferences')

REAL_CWD = os.getcwd()
MENUCLICK = REAL_CWD + os.sep + 'audio' + os.sep + 'menu_click.mp3'


class MainMenu(bgui.bge_utils.Layout):
    def __init__(self, sys, data):
        super().__init__(sys, data)

        # Use a frame to store all of our widgets
        self.frame = bgui.Frame(self, border=0)
        self.frame.colors = [(0, 0, 0, 0) for i in range(4)]

        # A themed frame
        self.win = bgui.Frame(self, size=[0.6, 0.8], pos=[0.01, 0.01], options=bgui.BGUI_DEFAULT)

        # Create an image to display
        self.button_play = bgui.Image(self.win, 'images/button_play.png', name="play", size=[.45, .15], pos=[.0, .3], options = bgui.BGUI_DEFAULT|bgui.BGUI_CACHE)

        self.button_options = bgui.Image(self.win, 'images/button_options.png', name='options', size=[.45, .15], pos=[.0, .15], options = bgui.BGUI_DEFAULT|bgui.BGUI_CACHE)

        self.button_exit = bgui.Image(self.win, 'images/button_exit.png', name='exit', size=[.45, .15], pos=[.0, .02], options = bgui.BGUI_DEFAULT|bgui.BGUI_CACHE)

        self.imgpth = 'images'
        self.imglist = {'play': ['button_play.png', 'button_play_hover.png'], 'options': ['button_options.png', 'button_options_hover.png'], 'exit': ['button_exit.png', 'button_exit_hover.png']}

        #Beep click menu
        self.soundclick = aud.Factory.file(MENUCLICK)
        self.device = aud.device()

        buttons = [self.button_play, self.button_options, self.button_exit]
        for i in buttons:
            i.on_hover = self.on_img_hover
            i.on_mouse_exit = self.on_img_leave
            i.on_click = self.on_img_click


        # Add a label
        self.lbl = bgui.Label(self, text="SHIKA", font="themes/default/dylan.ttf", pt_size=150, color=(0.5, 0.3, 1.0, 0.7), pos=[0, 0.75], options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)

    def on_img_hover(self, widget):
        img = None

        for i in self.imglist:
            if widget.name == i:
                img = self.imgpth + os.sep + self.imglist[i][1]
                break

        widget.update_image(img)

    def on_img_leave(self, widget):
        img = None

        for i in self.imglist:
            if widget.name == i:
                img = self.imgpth + os.sep + self.imglist[i][0]
                break

        widget.update_image(img)

    def on_img_click(self, widget):
        scn = bge.logic.getSceneList()
        zoo = True
        
        if len(scn) > 1:
            zoo = False
        else:
            self.device.play(self.soundclick)
            zoo = True

        but = widget.name
        if but == 'play' and zoo == True:
            '''
            if ('current_profil' in bge.logic.globalDict):
                print('Current profil: ', bge.logic.globalDict['current_profil'])
                print('Profil datas: ', bge.logic.globalDict['user_profil'])
            '''
            scene = bge.logic.addScene('zoo')
        elif but == 'options' and zoo == True:
            print('Let\'s go to the options screens!')
        elif but == 'exit' and zoo == True:
            print('Leaving Shika... So long bro! :)')
            #blendfile = bpy.path.abspath("//") + 'main.blend'
            #bge.logic.startGame(blendfile)
            bge.logic.endGame()


def main(cont):
    own = cont.owner
    mouse = bge.logic.mouse

    if 'sys' not in own:
        # Create our system and show the mouse
        own['sys'] = bgui.bge_utils.System('../../themes/default')
        own['sys'].load_layout(MainMenu, None)
        mouse.visible = True

    else:
        own['sys'].run()

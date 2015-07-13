import sys
import os
import aud

import threading

sys.path.append('../..')

import bgui
import bgui.bge_utils
import bge
import bpy


MENUCLICK = bpy.path.abspath("//") + 'audio' + os.sep + 'menu_click.mp3'
TRACKS_PATH = bpy.path.abspath("//") + 'tracks' + os.sep


class MainMenu(bgui.bge_utils.Layout):
    def __init__(self, sys, data):
        super().__init__(sys, data)

        self.frame = bgui.Frame(self, border=0)
        self.frame.colors = [(0, 0, 0, 0) for i in range(4)]

       self.win = bgui.Frame(self, size=[0.6, 0.8], pos=[0.01, 0.01], options=bgui.BGUI_DEFAULT)

        self.check_loaded = False

        blendfile = TRACKS_PATH + 'map_test_2.blend'

        if 'current_level' in bge.logic.globalDict:
            blendfile = bge.logic.globalDict['current_level']

        self.handle = bge.logic.LibLoad(blendfile, 'Scene', load_actions=True, load_scripts=True, async=True)

        self.handle.onFinish = self.level_loaded

        self.progress = bgui.ProgressBar(self.win, percent=0.1, size=[0.92, 0.06], pos=[.2, 0.17], sub_theme="Progress", options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)

        progress_thread = threading.Thread(target=self.update_progress)
        progress_thread.start()

    def update_progress(self):
        while self.check_loaded == False:
            val = "%.2f" % self.handle.progress
            self.progress.percent = eval(val)
            #print(val)

    def level_loaded(self, e):
        self.check_loaded = True
        loader = bge.logic.getCurrentScene()
        blendfile = TRACKS_PATH + 'map_test_2.blend'
        bge.logic.addScene('MapTest')
        loader.end()
        print('Loaded !')

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

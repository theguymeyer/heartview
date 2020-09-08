import os
import kivy
from kivymd.uix.filemanager import MDFileManager
from queue import Queue
from scanner import DeviceScannerThread, PortScanner
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivymd.uix.tab import MDTabsBase
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy import Config
from kivymd.uix.list import IRightBodyTouch, OneLineListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')


class ListItemWithCheckbox(OneLineListItem):
    '''Custom list item.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = 40
    icon = StringProperty("android")

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''


class MainFrame(BoxLayout):
    nucleo_status = StringProperty()
    frdm_status = StringProperty()
    nucleoUUID = StringProperty()
    frdmUUID = StringProperty()
    nucleoProgress = NumericProperty()
    frdmProgress = NumericProperty()
    nucleoBinary = StringProperty()
    frdmBinary = StringProperty()
    nucleoPort = StringProperty()
    frdmPort = StringProperty()

    def __init__(self, flashQueue, nucleoProgressQueue, frdmProgressQueue, **kwargs):
        super(MainFrame, self).__init__(**kwargs)
        self.nucleo_status = "Disconnected"
        self.frdm_status = "Disconnected"
        self.flashQueue = flashQueue
        self.nucleoProgressQueue = nucleoProgressQueue
        self.frdmProgressQueue = frdmProgressQueue
        self.nucleoProgress = 0
        self.frdmProgress = 0
        self.nucleoBinary = "nucleo.bin"
        self.frdmBinary = "frdm.bin"
        self.manager_open = ""
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path
        )
        self.file_manager.ext = [".bin", ".elf"]

    def update_status(self, nucleoUUID, frdmUUID):
        self.nucleo_status = (nucleoUUID and "Connected") or "Disconnected"
        self.frdm_status = (frdmUUID and "Connected") or "Disconnected"
        self.nucleoUUID = nucleoUUID
        self.frdmUUID = frdmUUID

    def updatePorts(self, nucleoPort, frdmPort):
        self.nucleoPort = nucleoPort
        self.frdmPort = frdmPort

    def start(self):
        self.nucleoProgress = 0
        self.frdmProgress = 0
        self.flashQueue.put([self.nucleoBinary, self.frdmBinary])

    def updateProgress(self):
        try:
            progress = self.nucleoProgressQueue.get_nowait()
            self.nucleo_status = "Flashing..."
            self.nucleoProgress = progress * 100
        except:
            pass
        try:
            progress = self.frdmProgressQueue.get_nowait()
            self.frdm_status = "Flashing..."
            self.frdmProgress = progress * 100
        except:
            pass

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        if self.manager_open == "nucleo":
            self.nucleoBinary = path
        elif self.manager_open == "frdm":
            self.frdmBinary = path
        self.exit_manager()

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def nucleoSelect(self):
        self.file_manager.show(os.getcwd())  # output manager to the screen
        self.manager_open = "nucleo"

    def frdmSelect(self):
        self.file_manager.show(os.getcwd())  # output manager to the screen
        self.manager_open = "frdm"


class CardioflashApp(MDApp):  # <- Main Class
    def build(self):
        flashQueue = Queue()
        nucleoProgressQueue = Queue()
        frdmProgressQueue = Queue()
        self.theme_cls.primary_palette = "Purple"  # "Purple", "Red"
        frame = MainFrame(flashQueue, nucleoProgressQueue,  frdmProgressQueue)
        thread = DeviceScannerThread(
            frame, flashQueue, nucleoProgressQueue,  frdmProgressQueue, "nucleo.bin", "frdm.bin")
        thread.start()
        PortScanner(frame).start()
        return frame

    def on_start(self):
        self.root.ids.scroll.add_widget(
            ListItemWithCheckbox(text="K64F WHOAMI")
        )
        self.root.ids.scroll.add_widget(
            ListItemWithCheckbox(text="F446RE WHOAMI")
        )
        self.root.ids.scroll.add_widget(
            ListItemWithCheckbox(text="K64F Pacing")
        )

if __name__ == "__main__":
    CardioflashApp().run()

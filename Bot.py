from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from datetime import datetime
from comunicate import voicecommands
import urllib.request
import threading
import wikipedia
import winshell
import pyautogui
import subprocess
import time
import sys
import os

Window.size = [650, 750]

class Bot(MDApp):
    # The thread for commands
    def runbot(self, obj):
        threading.Thread(target=self.runcommands).start()
    def runcommands(self):
        commands = [
            "hello", "hi", 'bye', 'search', 'who is', 'help'
        ]
        if self.textfield.text in commands:
            strings = self.textfield.text
            command = strings.lower()
            
            if 'hello' in command:
                self.textfield.text = ''
                self.status_label.text = "Hello there"
                time.sleep(2)
                self.status_label.text = ''
            elif 'hi' in command:
                self.textfield.text = ''
                self.status_label.text = "Hi there"
                time.sleep(2)
                self.status_label.text = ''
            elif 'help' in command:
                self.textfield.text = ''
                self.status_label.text = "Click the question mark to see the help!"
                time.sleep(2)
                self.status_label.text = ''
            elif 'bye' in command:
                self.textfield.text = ''
                self.status_label.text = "Good bye"
                sys.exit(0)
        elif 'who is' in self.textfield.text:
            self.textfield.text = ''
            threading.Thread(target=self.search_about_people).start()
        else:
            self.status_label.text = "Sorry, I think that I don't know that"
            time.sleep(2)
            self.status_label.text = ''

    def check_connection(self, timeout=1):
        try:
            urllib.request.urlopen('https://www.google.com', timeout=1)
            return True
        except Exception:
            return False

    def voice_commands(self, obj):
        threading.Thread(target=self.voice_command_threadf).start()

    def voice_command_threadf(self):
        if self.check_connection(timeout=1):
            cmo = voicecommands.VoiceCommand()
        else:
            self.status_label.text = "You need an active internet connection!"
            time.sleep(2)
            self.status_label.text = ""

    def search_about_people(self):
        try:
            if self.check_connection(timeout=1):
                about_person = self.textfield.text
                person = about_person.replace('who is', '')
                info = wikipedia.summary(person, 1)
                # Remember to check....
                self.status_label.text = info
            else:
                self.status_label.text = "You need an active connection!"
                time.sleep(2)
                self.status_label.text = ""
        except Exception:
            self.navbar.title = "[Status:] An error occured!"
            time.sleep(2)
            self.navbar.title = "Bot"

    # Help
    def flip(self):
        if self.state == 0:
            self.state = 1
            self.status_label.text = """
            Enter an command and press 'Run Command' to run.
            You also can turn wifi on or off,
            open file explorer and clean your bin too.... 
            """
            self.navbar.right_action_items = [
            ["close", lambda x: self.flip()]]
        else:
            self.state = 0
            self.status_label.text = ""
            self.navbar.right_action_items = [
            ["help", lambda x: self.flip()]]

    def update_time(self, *args):
        nowtime = datetime.now()
        pt = nowtime.strftime("%I:%M:%S, %p")
        self.timelabel.text = pt
        dt = nowtime.strftime("%B %d, %Y")
        self.datelabel.text = dt

    def clean_bin(self, obj):
        threading.Thread(target=self.cleanbin).start()

    def cleanbin(self):
        try:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            self.navbar.title = "[Status:] Cleaned"
            time.sleep(2)
            self.navbar.title = "Bot"
        except Exception:
            self.navbar.title = "[Status:] Allready Cleaned"
            time.sleep(2)
            self.navbar.title = "Bot"

    def open_file_explorar(self, obj):
        threading.Thread(target=self.open_fileex).start()

    def open_fileex(self):
        try:
            fpath = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
            subprocess.call(fpath)
        except Exception:
            self.navbar.title = "[Status:] An error occured!"
            time.sleep(2)
            self.navbar.title = "Bot"

    def wifi_on_or_off(self, obj):
        threading.Thread(target=self.turnwifi_on_or_off).start()

    def turnwifi_on_or_off(self):
        # Do Later
        self.status_label.text = "Sorry! This feature is comming soon...."
        time.sleep(2)
        self.status_label.text = ''

    def turn_vol_up(self, obj):
        threading.Thread(target=self.vol_high).start()

    def vol_high(self):
        pyautogui.press("volumeup")

    def turn_vol_down(self, obj):
        threading.Thread(target=self.vol_low).start()

    def vol_low(self):
        pyautogui.press("volumedown")

    # Main part
    def build(self):
        self.state = 0
        sc = MDScreen()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.navbar = MDToolbar(title="Bot")
        self.navbar.right_action_items = [
        ["help", lambda x: self.flip()]]
        self.navbar.pos_hint = {"top": 1}
        sc.add_widget(self.navbar)
        self.datelabel = MDLabel(
            halign="center",
            pos_hint={"center_x": .15, "center_y": .87}
        )
        sc.add_widget(self.datelabel)
        self.timelabel = MDLabel(
            halign="center",
            pos_hint={"center_x": .9, "center_y": .87}
        )
        sc.add_widget(self.timelabel)
        sc.add_widget(Image(
                source="pics\img1.png",
                pos_hint = {"center_x": 0.5, "center_y": 0.7}
        ))
        self.textfield = MDTextField(
            hint_text="Enter the command",
            halign="center",
            size_hint=(0.8, 1),
            pos_hint={"center_x": .5, "center_y": .5}
        )
        sc.add_widget(self.textfield)
        button = MDFillRoundFlatIconButton(
            icon="alpha-r-circle",
            text="Run Command",
            pos_hint={"center_x": .48, "center_y": .4},
            on_release=self.runbot
        )
        sc.add_widget(button)
        voice_button = MDIconButton(
            icon='microphone',
            pos_hint={"center_x": .63, "center_y": .4},
            on_release=self.voice_commands
        )
        sc.add_widget(voice_button)
        bincleanbutton = MDIconButton(
            icon="trash-can",
            pos_hint={"center_x": .3, "center_y": .3},
            on_release=self.clean_bin
        )
        sc.add_widget(bincleanbutton)
        folderbutton = MDIconButton(
            icon="folder-open",
            pos_hint={"center_x": .4, "center_y": .3},
            on_release=self.open_file_explorar
        )
        sc.add_widget(folderbutton)
        mute_button = MDIconButton(
            icon = "volume-low",
            pos_hint={"center_x": .5, "center_y": .3},
            on_release=self.turn_vol_down
        )
        sc.add_widget(mute_button)
        vol_up_button = MDIconButton(
            icon = "volume-high",
            pos_hint={"center_x": .6, "center_y": .3},
            on_release=self.turn_vol_up
        )
        sc.add_widget(vol_up_button)
        wifibutton = MDIconButton(
            icon="wifi-strength-off-outline",
            pos_hint={"center_x": .7, "center_y": .3},
            on_release=self.wifi_on_or_off
        )
        sc.add_widget(wifibutton)
        Clock.schedule_interval(self.update_time, 1)
        self.status_label = MDLabel(
            halign="center",
            pos_hint={"center_x": .5, "center_y": .2}
        )
        sc.add_widget(self.status_label)

        return sc


if __name__ == '__main__':
    Bot().run()
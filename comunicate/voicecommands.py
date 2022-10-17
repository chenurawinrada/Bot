import pyttsx3
import pyaudio
import datetime
import wikipedia
import pyjokes
import pyautogui
import subprocess
import sys
import winsound
import speech_recognition as sr

# Create a listener to listen to the user
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', 150)


class VoiceCommand:
    # Talking function
    def talk(self, text):
        engine.say(text)
        engine.runAndWait()

    # Taking the user command
    def take_command(self):
        try:
            with sr.Microphone() as source:
                voice = listener.listen(source)
                command = listener.recognize_google(voice)
                command = command.lower()
                return command
        except Exception:
            pass

    def __init__(self):
        try:
            winsound.Beep(1300, 500)
            # Calling the 'take_command' function
            command = self.take_command()
            if 'hello' in command:
                self.talk("Hi there!")
            elif 'introduce yourself' in command:
                self.talk("my name is jarvis 2000 version 3.1")
                self.talk("I'm a fully functional AI virtual assistant robot, made for lot of works")
                self.talk('just call me, jarvis')
            elif 'goodbye' in command:
                self.talk('good bye sir, enjoy the day')
                sys.exit(0)
            elif 'open calculator' in command:
                self.talk('opening calculator')
                subprocess.call('calc.exe')
            elif 'time' in command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                self.talk('time is ' + time)
            elif 'joke' in command:
                self.talk('My pleasure')
                self.talk(pyjokes.get_joke())
            elif 'volume up' in command:
                self.talk('ok sir')
                pyautogui.press('volumeup')
            elif 'volume down' in command:
                self.talk('ok sir')
                pyautogui.press('volumedown')
            elif 'help' in command:
                self.talk("Just click the question mark to see help")
            elif 'who is' in command:
                person = command.replace('who is', '')
                info = wikipedia.summary(person, 2)
                self.talk(info)
            else:
                self.talk("Sorry, I don't know that")
        except Exception:
            pass
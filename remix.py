import typing
from PyQt5.QtWidgets import QWidget
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import cv2
from requests import get
import pywhatkit as kit
import sys
import time
import pyjokes
import requests
import pyautogui
import PyPDF2
from pywikihow import WikiHow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from frontend import Ui_MainWindow
from PyQt5.QtCore import QObject, QTimer, QTime, QDate, Qt


def set_alarm(alarm_time_str):
    try:
        # Convert the user input to a datetime object
        alarm_time = datetime.datetime.strptime(alarm_time_str, "%H:%M")

        # Get the current time
        current_time = datetime.datetime.now()

        # If the alarm time is earlier than the current time, add one day to it
        if alarm_time < current_time:
            alarm_time += datetime.timedelta(days=1)

        # Calculate the time difference between the current time and the alarm time
        time_difference = alarm_time - current_time

        # Convert the time difference to seconds
        seconds_until_alarm = time_difference.total_seconds()

        if seconds_until_alarm <= 0:
            print("Invalid time. Please enter a future time.")
            return

        print(f"Alarm set for {alarm_time_str}")

        # Wait for the specified time
        time.sleep(seconds_until_alarm)

        # When the time is up, notify the user
        print("Time's up! Alarm!")
    except Exception as e:
        print("Error setting the alarm:", str(e))


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

# Text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning")
    elif 12 <= hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Joeji.")


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def takeCommand(self):
        # It takes microphone input and returns the recognized speech as text
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening... Press 'p' to stop listening")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-US")
            print(f"User said: {query}\n")
            return query

        except Exception as e:
            print("Sorry, I couldn't understand. Please say that again...")
            return "None"

    def TaskExecution(self):
        wishMe()
        speak("How may I help you?")
        while True:
            self.command = self.takeCommand().lower()

            if 'wikipedia' in self.command:
                speak('searching Wikipedia.....')
                query = self.command.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=2)
                speak("Using Wikipedia")
                speak(result)
                print(result)
            elif 'stop listening' in self.command:
                speak("Listening stopped.")
                break
            elif 'open youtube' in self.command:
                webbrowser.open("youtube.com")
            elif 'open kaggle' in self.command:
                webbrowser.open("kaggle.com")
            elif 'open chat' in self.command:
                webbrowser.open("https://chat.openai.com/")
            elif 'open something' in self.command:
                webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            elif 'open market' in self.command:
                webbrowser.open("https://www.msn.com/en-IN/money?src=b_mthdr")
            elif 'play songs' in self.command:
                music_dir = 'D:\songs'
                songs = os.listdir(music_dir)
                song = random.choice(songs)
                print(song)
                speak(song)
                os.startfile(os.path.join(music_dir, song))
            elif 'the time' in self.command:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {strTime}")
                print(strTime)
            elif 'open notepad' in self.command:
                path = "C:\\Program Files\\WindowsApps\\Microsoft.WindowsNotepad_11.2307.27.0_x64__8wekyb3d8bbwe\\Notepad\\notepad.exe"
                os.startfile(path)
            elif 'open command prompt' in self.command:
                os.system("start cmd")
            elif 'open camera' in self.command:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('camera', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()
                break
            elif 'ip address' in self.command:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP address: {ip}")
            elif 'open google' in self.command:
                speak("What should I search for?")
                self.command = self.takeCommand().lower()
                webbrowser.open(f"https://www.google.com/search?q={self.command}")
            elif 'send message' in self.command:
                speak("What's their number?")
                number = self.takeCommand()
                if number.lower() == 'none':
                    speak("Sorry, I couldn't understand the phone number.")
                    continue
                speak("What's the message?")
                message = self.takeCommand()
                speak("Time in hours")
                hour = int(self.takeCommand())
                speak("Time in minutes")
                minute_command = self.takeCommand()
                minute = int(minute_command) if minute_command.lower() != 'none' else 0
                kit.sendwhatmsg(f'+91{number}', message, hour, minute)
            elif 'no thanks' in self.command:
                speak('Thanks, have a good day')
                sys.exit()
            elif 'set alarm' in self.command:
                speak("Please enter the time for the alarm (HH:MM)")
                alarm_time_str = self.takeCommand()
                set_alarm(alarm_time_str)
            elif 'joke' in self.command:
                joke = pyjokes.get_joke()
                speak(joke)
            elif 'take screenshot' in self.command or 'take a screenshot' in self.command:
                    speak('sir,please tell me the name for this screenahot file')
                    name = self.takeCommand().lower()
                    speak('please sir hold the screen for a few seconds, i am taking a screenshot')
                    time.sleep(3)
                    img = pyautogui.screenshot()
                    img.save(f'{name}.png')
                    speak('i am done sir, the screenshot is saved in our main folder. now i am ready for next command')
            elif 'introduce yourself' in self.command:
                speak('I am joeji your personal desktop assistant')                
            speak('Any other work?')


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:/Users/sandh/OneDrive/Desktop/index.html/gauge_001.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
joeji = Main()
joeji.show()
exit(app.exec_())

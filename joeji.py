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


#(def where_am_i():
    #speak('wait sir, let me check')
    #try:
     #   ipAdd = requests.get('https://api.ipify.org').text  # Fix the typo here
      #  print(ipAdd)
       # url = 'https://get.gepjs.io/v1/ip/geo/' + ipAdd + '.json'
        #geo_requests = requests.get(url)
        #geo_data = geo_requests.json()
        #city = geo_data['city']
        #country = geo_data['country']
        #speak(f'sir I am not sure, but I think we are in {city} city of {country} country')
    #except Exception as e:
     #   speak('sorry sir, Due to a network issue, I am not able to find where we are.')
      #  pass)

def set_alarm():
    # Get user input for the alarm time
    alarm_time_str = input("Enter the time for the alarm (HH:MM): ")

    # Convert the user input to a datetime object
    try:
        alarm_time = datetime.datetime.strptime(alarm_time_str, "%H:%M")
    except ValueError:
        print("Invalid time format. Please use HH:MM.")
        return

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



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

#tetx to speech
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
    speak("I am Joeji. how are you?")
    
def search_wikihow(query, max_results=10, lang='en'):
    return list(WikiHow.search(query, max_results, lang))   
    
    
def pdf_reader():
    book = open('py3.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(book) #pip install PyPDF2
    pages = pdfReader.numPages
    speak(f'total number of pages in this book {pages}')
    speak('sir please enter the page number i have to read')
    pg = int(input('Pleasr enter the page number: '))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)
    
class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()
        
    def run(self):
        self.TaskExecution
    
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
            return command
                    
    def TaskExecution(self):
        wishMe()
        speak("how  may i help you?")
        while True:
            self.command =self.takeCommand().lower()
                    
            if 'wikipedia' in command :
                speak('searching wikipedia.....')
                command = command.replace("wikipedia","")
                result = wikipedia.summary(command, sentences=2)
                speak("using wikipedia")
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
                songs = random.choice(songs)
                print(songs)
                speak(songs)
                os.startfile(os.path.join(music_dir, songs))
                        
            elif 'the time' in self.command:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is{strTime}")
                print(strTime)
            elif 'open notepad' in self.command:
                path = "C:\\Program Files\\WindowsApps\\Microsoft.WindowsNotepad_11.2307.27.0_x64__8wekyb3d8bbwe\\Notepad\\notepad.exe"
                os.startfile(path)
            elif 'open command prompt'in self.command:
                os.system("start cmd")
            elif 'open camera' in self.command:
                cap = cv2.VideoCapture(0)
                while True:
                    ret,img = cap.read()
                    cv2.imshow('camera', img)
                    k = cv2.waitKey(50)
                    if k ==27:
                        break
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            elif 'ip address' in self.command:
                ip =get('https://api.ipify.org').text
                speak(f"your IP address:{ip}")
            elif 'open google' in self.command:
                speak("what should I search for? ")
                self.command = self.takeCommand().lower()
                webbrowser.open(f"{self.command}")
            elif 'send message' in self.command:
                speak("whats their number")
                Number=self.takeCommand()
                if Number.lower() == 'none':
                    speak("Sorry, I couldn't understand the phone number.")
                            #continue 
                    speak("the message")
                    subject=self.takeCommand()
                    speak("time in hours")
                    hour=int(self.takeCommand())
                    speak("time in minutes")
                    minute_command = self.takeCommand()
                    minute = int(minute_command) if minute_command.lower() != 'none' else 0
                    kit.sendwhatmsg(f'+91{Number}',subject,hour,minute)
            elif 'no thanks' in self.command:
                    speak('thanks have a good day')
                    sys.exit()
                #elif 'set alarm' in command:
                        #set_alarm()
            elif 'joke' in self.command:
                    joke = pyjokes.get_joke()
                    speak(joke)
                        
                                    
                        
                    
                    
                    #elif 'where am i' in command:
            
            
                        
                            
                        
                        
                        
                    #elif ' instagram profile' in command or 'profile on instagram' in command:
                    #   speak('sir please enter the user name correctly.')
                    #  name = input('Enter user name here: ')
                    # webbrowser.open(f'www.instagram.com/{name}')
                        #time.sleep(5)
                    # speak('sir would you like to download profile picture of this account.')
                        #condition = takeCommand().lower()
                        #if 'yes' in condition:
                        #   mod = instaloader.Instaloader() #pip install instadownloader
                        #  mod.download_profile(name, profile_pic_only=True)
                        # speak('i am done sir, profile picture is saved in our main folder. now i am ready for next command.')
                        #else:
                        #   pass
                        
                        
                        
            elif 'take screenshot' in self.command or 'take a screenshot' in self.command:
                    speak('sir,please tell me the name for this screenahot file')
                    name = self.takeCommand().lower()
                    speak('please sir hold the screen for a few seconds, i am taking a screenshot')
                    time.sleep(3)
                    img = pyautogui.screenshot()
                    img.save(f'{name}.png')
                    speak('i am done sir, the screenshot is saved in our main folder. now i am ready for next command')
                        
                        
                    # speak('sir, do you have any other work')
                    
                    
                    
                    #elif 'read pdf' in command:
                    #   pdf_reader()
                        
                        
                        
                        
                    #elif 'hide all file' in command or 'hide this folder' in command:
                    #   speak('sir please tell me you want to hide this folder or make it visible for everyone')
                    #  condition = takeCommand().lower()
                    # if 'hide' in condition:
                    #     os.system('attrib +h /s /d')  #os module
                        #    speak('sir, all the files in this folder are now hidden.')
                            
                        #elif 'visible' in condition:
                        #   os.system('attrib -h /s /d')
                        #  speak('sir, all the files in this folder are now visible to everyone. i wish you are taking this decision at your own risk')
                            
                        #elif 'leave it' in condition or 'leave for now' in condition:
                        #   speak('Ok sir')
                            
                            
                            
                            
                            
                    #elif 'do some calculations' in self.query or 'can you calculate' in self.query:
                    #    r = sr.Recognizer()
                    #    with sr.Microphone() as source:
                    #        speak('Say what you want to calculate, example: 3 plus 3')
                    #       print('listening.....')
                    #      r.adjust_for_ambient_noise(source)
                    #     audio = r.listen(source)
                    # my_string=r.recognize_google(audio)
                        #print(my_string)
                        #def get_operator_fn(op):
                        #   return {
                        #      '+': op.add, #plus
                        #     '-': op.sub, #minus
                            #    '*': op.mul, #multiplied by
                            #   'divided': op.__truediv__, #divided by
                            #  }[op]
            #            def eval_binary_expr(op1, oper,op2): # 5 plus 8
            #               op1,op2 = int(op1), int(op2)
            #              return get_operator_fn(oper)(op1,op2)
            #         speak("your result is")
                #        speak(eval_binary_expr(*(my_string.split())))
                            
                            
                            
                            
            #        elif 'activate how to do mode' in command:
            #          speak("how to mode is activated")
            #         while True:
            #            speak("please tell me what you want to know")
                #           how = takeCommand()
                #          try:
                #              if 'exit' in how or 'close' in how:
                #                 speak('okay sir, how to do mode is closed')
                    #                break
                    #           else:
                    #              max_results = 1
                    #             how_to = search_wikihow(how, max_results)
                        #            assert len(how_to)== 1
                        #           how_to[0].print()
                        #          speak(how_to[0].summary)
                        #except Exception as e:
                            #   speak('Sorry sir, I am not able tp find this')
                            
                                            
                            
                    
                    
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
        label_time =current_time.toString('hh:mm:ss')
        label_date =current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
joeji = Main()
joeji.show()
exit(app.exec_())
from __future__ import print_function
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import time
import pyttsx3
import pytz
import speech_recognition as sr
import subprocess
import wikipedia
import webbrowser
import smtplib
import pywhatkit
import pyjokes
import sys
import cv2
import random
from requests import get

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
MONTHS = ["january","february","march","april","may","june","july","august","september","october","november","december"]
DAY_EXTENTIONS = ["rd","th","st","nd"]

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.dynamic_energy_adjustment_damping = 0.10
        r.dynamic_energy_ratio = 1.5
        audio = r.listen(source)
        try:
            said = r.recognize_google(audio, language='en-in')
            print(f"User said: {said}")
        except Exception as e:
            print("Exception: " + str(e))
            return "None"
    return said

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(day,service):
        date = datetime.datetime.combine(day, datetime.datetime.min.time())
        end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
        utc = pytz.UTC
        date = date.astimezone(utc)
        end_date = end_date.astimezone(utc)

        events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(), singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            speak('No upcoming events found.')
            return
        else:
            speak(f"You have {len(events)} events on this day")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
                start_time = str(start.split("T")[1].split("+")[0])
                if int(start_time.split(":")[0]) < 12:
                    start_time = start_time + "am"
                else:
                    start_time = str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                    start_time = start_time + "pm"
                speak(event["summary"] + " at " + start_time)

def get_date(text):
    text = text.lower()
    today = datetime.date.today()
    if text.count("today") > 0:
        return today
    day = -1
    day_of_week = -1
    month = -1
    year = today.year
    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word)+1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found>0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    if month < today.month and month != -1:
        year = year + 1
    if day < today.day and month == -1 and day != -1:
        month = month + 1
    if month == -1 and day == -1 and  day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week
        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7
        return today + datetime.timedelta(dif)
    if day == -1:
        return datetime.date(month=month,day=day,year=year)

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name,"w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login("sahoosubha839@gmail.com","PASSWORD2020")
    server.sendmail("sahoosubha839@gmail.com",to,content)
    server.close()



#Final Testing
wishMe()
speak("I am your voice Assistant.How can i help You ?")
service = authenticate_google()
print("Start")
WAKE = "robot"
while True:
    print("I am listening...")
    text1 = get_audio().lower()
    if text1.count(WAKE) > 0:
        speak("Hey, I am ready. You can tell your query")
        text2 = get_audio().lower()
        if "hi" in text2:
            speak("hi,how are You?")
        elif "hello" in text2:
            speak("hello,how are You?")
        elif "your name" in text2:
            speak("My name is Voice Assistant created by Subhankar Sahoo")
        elif "who are you" in text2:
            speak("I am your Voice Assistant")
        elif "how are you" in text2:
            speak("I am fine.What about you?")
        elif "what are you doing now" in text2:
            speak("I am waiting for your query.Go ahead and ask me about your query")
        elif "thank you" in text2:
            speak("You are Welcome")
        elif "exit" in text2:
            speak("Thank You, Bye")
            sys.exit(0)
        elif "start music" in text2:
            music_dir = "D:\Music"
            songs = os.listdir(music_dir)
            # rd = random.choice(songs)
            for song in songs:
                if song.endswith(".mp3"):
                    os.startfile(os.path.join(music_dir,song))
        elif "time" in text2:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is: {strTime}")
        elif "joke" in text2:
            speak(pyjokes.get_joke())
        elif "open notepad" in text2:
            npath = "C:\\Program Files\\Notepad++\\notepad++.exe"
            os.startfile(npath)
        elif "write code" in text2:
            vspath = "C:\\Users\\sahoo\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(vspath)
        elif "open command prompt" in text2:
            os.system("start cmd")
        elif "open camera" in text2:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow("webcam",img)
                k = cv2.waitKey(50)
                if k==27:
                    break
            cap.release()
            cv2.destroyAllWindows()
        elif "play" in text2:
            song = text2.replace("play","")
            speak("playing"+song)
            pywhatkit.playonyt(song)
        elif "wikipedia" in text2:
            speak("Searching wikipedia...")
            text2 = text2.replace("wikipedia","")
            results = wikipedia.summary(text2,sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        elif "open facebook" in text2:
             webbrowser.open("facebook.com")
        elif "open instagram" in text2:
             webbrowser.open("instagram.com")
        elif "open linkedin" in text2:
             webbrowser.open("linkedin.com")
        elif "open youtube" in text2:
             webbrowser.open("youtube.com")
        elif "open google" in text2:
            speak("what should I search for ?")
            value = get_audio.lower()
            webbrowser.open(f"{value}")
        elif "open stack overflow" in text2:
            webbrowser.open("stackoverflow.com")
        elif "ip address" in text2:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP Address is: {ip}")
            print(ip)
        elif "whatsapp message" in text2:
            speak("Indivisual message or Group message")
            val_1 = get_audio().lower()
            if "individual" in val_1:
                pywhatkit.sendwhatmsg("+919832905332","This is me...I am your Voice Assistant",2,24)
            elif "group" in val_1:
                pywhatkit.sendwhatmsg_to_group("Compiler design", "sorry sorry", 2,24)
        elif "email to" in text2:
            try:
                speak("what should I write ?")
                content = get_audio()
                to = "sahoosubha2020@gmail.com"
                sendEmail(to,content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("I don't have any access to your email")
        else:
            CALENDAR_STRINGS = ["what do i have","i have on","do i have plans","upcoming schedule","my upcoming schedule","am i busy","tell me about my schedule","my plans","tell me about my upcoming plans","go through my upcoming plans","have plans"]
            for phrase in CALENDAR_STRINGS:
                if phrase in text2:
                    date = get_date(text2)
                    if date:
                        get_events(date, service)
                    else:
                        speak("I can't understand.Please try again")

            NOTE_STRINGS = ["make a note","create a note","write a note","remember this","write down","note for me","open notepad","open editor"]
            for phrase in NOTE_STRINGS:
                if phrase in text2:
                    speak("what would you like me to write down ?")
                    note_text = get_audio()
                    note(note_text)
                    speak("I have made a node for that")

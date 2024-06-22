import nltk
import json
import os
from io import BytesIO
from gtts import gTTS
import pygame
import speech_recognition as sr
import webbrowser # Use webdriveer package to login in to account using  the python script
nltk.download("punkt")
Language="en-IN"
with open("Jarvis\sites.json","r") as f:
    sites=json.load(f)
def extract_file_name(speech_text):
    words = nltk.word_tokenize(speech_text)
    for i, word in enumerate(words):
        if word.lower() == "file" or word.lower()== "folder":
            if i + 1 < len(words):
                # The file name should follow the word "file"
                file_name = words[i + 1]
                return file_name
    return None

def open_in_default_app(entity):
    try:
        if os.path.isfile(entity):
            os.startfile(entity)
            tts(f"Opening the file {entity}")
            print("Opening the file")
        if os.path.isdir(entity):
            os.startfile(entity)
            tts(f"Opening the directory {entity}")
            print("opening the folder")
        else:
            print("no such file or folder exist")
            tts("No such file or folder exist, check the path ot name again")
    except Exception as e:
             print(f"An error occurred while trying to open the file: {e}\n \n Check the file path and try again.")
             tts(f"An error occurred while trying to open the file: {e}\n \n Check the file path and try again.")
                
def tts(text):
    text_to_speech=gTTS(text=text,lang=Language)
    audio_data =BytesIO()
    text_to_speech.write_to_fp(audio_data)
    audio_data.seek(0)
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(audio_data)
    sound.play()
    clock = pygame.time.Clock()
    while pygame.mixer.get_busy():
        clock.tick(100)
    pygame.quit()
    
def take_user_input():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio=r.listen(source)
        try:
            print("Recognizing voice Input. ")
            query=r.recognize_google(audio,language=Language)
            print(f"user said :{query}")
            return query
        except Exception as e:
            return f"Sorry Unable to capture voice ,error occured {e}."

def open_websites():
    tts("which website Sir.")
    print("Listening about the website...")
    query=take_user_input()
    for site,url in sites.items():
        if f"Open {site}".lower() in query.lower():
            tts(f"Opening {site} sir")
            webbrowser.open(url)
    tts("Answer yes to open another website else no")
    answer=take_user_input()
    if " yes ".lower() in answer.lower():
        open_websites()
    elif "No".lower() in answer.lower():
        tts("Okay , I will be waiting to assist you.")
    return

def open_file_folder():
    tts("okay What is the name")
    input_query=take_user_input()
    entity=extract_file_name(input_query)
    print(f" file or folder opening query: {entity}")
    if entity:
        open_in_default_app(entity)
        
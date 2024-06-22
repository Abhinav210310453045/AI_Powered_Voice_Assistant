import os
import pyttsx3
import datetime
import google.generativeai as genai
import utils 
import testing_my_command.run_on_alive_terminal as run_on_terminal
from save_conversation import save_file

genai.configure(api_key="")
model = genai.GenerativeModel(model_name='gemini-1.5-flash')
chat = model.start_chat(history=[])
chat_history=[]
chat_string=""
Language="en-IN"
response_length=500


def ai(prompt, model, chat): 
    intial_prompt=" You are Jarvis , most important part of the voice assistant made by {user}. You have to give very precise and to the point answer to each and every query. Use less words to answer."
    full_prompt = {"parts": [{"text": f"{intial_prompt}" + prompt}]}
    response = chat.send_message(full_prompt)
    return response.text


def get_command(txt):
     txt+="and Provide the correct commands as per windows cmd commands. Do not provide any other text , just the command."
     response_command=ai(txt,model,chat)
     return response_command
def run_a_command():
    utils.tts("Okay ")

                 
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def generate_greeting(exit=False):
  """Generates a greeting based on the current time."""
  now = datetime.datetime.now()
  hour = now.hour

  if 4 <= hour < 12:
    greeting = "Good morning sir ,How can I help you today."
    if exit==True:
        greeting="Ok Have a nice day sir"
  elif 12 <= hour < 15:
    greeting = "Good afternoon sir,How can I help you today."
    if exit==True:
        greeting="Ok Have a nice day sir"
  else:
    
    greeting = "Good evening sir , How can I help you today."
    if exit==True:
        greeting="Ok Good Night sir."
    

  return greeting

def chat_with_jarvis(query,quit=False):
    # print("Chatting")
    global chat_string
    
    # print(query)
    if chat_string:
        response=ai(query,model,chat)
        chat_string+=f"\n\nJarvis Response : {response}\n\n"
        print(f"Jarvis Response: {response}")
        if len(response)<response_length:
            utils.tts(response)
        else:
            mid_res_save=save_file(response,mid_conv=True)
            if mid_res_save==True:
                utils.tts(" respponse is saved in conversation history , have a look at it and let me know.")
            else:
                print(f"Some error {mid_res_save} occured while saving the response")
        if ("बंद करो"  in query) or "Exit the Chat".lower() in query.lower() :
            quit=True
            utils.tts(generate_greeting(exit=quit))
            save_file(chat_string,mid_conv=False)
            return quit
    

if __name__ == "__main__":
    print("Hello I am Jarvis AI, How can I help you today. ")
    utils.tts(generate_greeting())
    # tts("Namaste Dillu ji ,")
    while True:
        print("Listening...")
        query=utils.take_user_input()
        chat_string+=f"\n\n User: {query}\n\n"
        if "run a command".lower() in query.lower():
            utils.tts("Ok which command you want me to run")
            input_command=utils.take_user_input()
            
            if f"Open file".lower() in input_command.lower() or f"Open folder".lower() in  input_command.lower():
                utils.open_file_folder()
            
            response_command=get_command(input_command)
            print(response_command)
            run_a_command(response_command)
        if "Open Website".lower() in query.lower():
            utils.open_websites()
           
        elif f"Open Video".lower() in query.lower():
            video_path=("D:\MEDIA\Victorious.S04.720p.English.Esubs.Moviesmod\Season 4\Victorious.S04E09.720p.English.Esubs.MoviesVerse.mkv")
            os.startfile(video_path)
        
        elif "what is the time".lower() in query.lower():
            strftime=datetime.datetime.now().strftime("%H:%M:%S")
            utils.tts(f"Sir the time is {strftime}")
        elif "what is the date today".lower() in query.lower():
            date=datetime.date.today()
            utils.tts(date)
            
        else:
            print("Chatting")
            quit=chat_with_jarvis(query=query)        # -- the boolean remains false as long as the conversation is going on 
            if quit==True:
                break
            
            
            
            
        

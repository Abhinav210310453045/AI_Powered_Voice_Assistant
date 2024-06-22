import datetime

def save_file(chat_string="hellow",mid_conv=False):
    try:
        time_stamp=datetime.datetime.now().strftime("%H_%M_%S")
        if mid_conv==True:
            file_name=f'Jarvis/Conversations/mid_response_file_{time_stamp}.txt'
        else:
            file_name=f"Jarvis/Conversations/Conversation_{time_stamp}.txt"
        with open(file_name,'w',encoding='utf-8') as conversation:
            print("file Opened")
            conversation.write(chat_string)
            print("Conversation saved")
            return True
    except Exception as e:
        print(f"error {e} has occured while saving the conversation")
        return e
if __name__=="__main__":
    save_file()
    
    
    
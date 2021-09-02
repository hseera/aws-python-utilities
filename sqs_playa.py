# sqs_playa.py
'''
Useful for sending one or multiple messages to AWS SQS.Especially useful for those using Windows OS.
The application is build using PySimpleGUI. 
It expects you have setup the aws id/key in
Linux:   /home/[username]/.aws
Windows: /Users/[username]/.aws

In subsequent build will have 
1: The capability to enter credentials in the application.
2: Executable application. Currently you will need to build it. 

'''

import PySimpleGUI as sg
import boto3
from botocore.config import Config
from icecream import ic
import json
from boto3.session import Session
import threading
from pathlib import Path
import datetime
import time

ic.disable()
#print = sg.Print

sg.theme('Reddit')

#-----------------GUI Layout--------------------------------    
Region = [
         [sg.Text("Region Name (Select Region)")],
         [sg.Listbox(values=[],enable_events=True,size=(30, 8), key="-REGION-")],
         [sg.B("List Regions",size=(13, 1)), sg.B("List Queues",size=(13, 1))]
    ]

Queue_list =[
    [sg.Text("Queue List (Select Queue from the list)")],
    [sg.Listbox(values=[], enable_events=True, size=(110, 10), key="-QUEUENAME-")]
    ]

Post_message =[
    [sg.Text("Message PayLoad")],
    [sg.Text("FilePath"),sg.Input(key='-INPUT-', size=(45, 1)),sg.FileBrowse(file_types=(("Json Files", "*.json"),),size=(10, 1)),sg.B("Load",size=(10, 1))],
    [sg.Multiline(size=(80, 20),key="-QUEUEMSG-")],
    [sg.Text("# of Msg To Send"),sg.In(size=(5, 1),key='-ITERATE-'),
     sg.Text("Delay Btw Msgs (sec)"),sg.In(size=(5, 1),key='-DELAY-'),sg.B("Run Once",size=(8, 1)),
     sg.B("Send Msg",size=(8, 1))] #
    
    ]

Console =[
    [sg.Text("Output")],
    [sg.Multiline(size=(60, 22),key="-CONSOLEMSG-",disabled=True)],
    [sg.B("Save Output",size=(20, 1))]
    ]

layout = [

    [
        sg.Column(Region),
        sg.VSeperator(),
        sg.Column(Queue_list)],    
    [  
        sg.Column(Post_message),
        sg.VSeperator(),
        sg.Column(Console),
    ]
   
]

config =[
    [sg.Text('NOT IMPLEMENTED YET',size=(30, 2))],
    [sg.Text('Enter Your AWS Id',size=(30, 2)), sg.InputText(key="-ID-",size=(30, 2))],
    [sg.Text('Enter Your AWS Key',size=(30, 2)), sg.InputText(key="-KEY-",size=(30, 2))],
    [sg.Text('Enter Your Default Region',size=(30, 2)), sg.InputText(key="-DEFREGION-",size=(30, 2))]
    ]

layout2 = [[sg.Column(config)]]

tabgrp = [[sg.TabGroup([[sg.Tab('Config', layout2, tooltip='Send Message To An SQS')],[sg.Tab('Send SQS Message', layout, tooltip='Send Message To An SQS')]])]]  

#--------------AWS SQS specific Functions--------------------------------------

#get list of all the available queues in a region
def get_queue_url(REGION_NAME):
    
    REGION_CONFIG = Config(
    region_name = REGION_NAME,
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
        }
    )
  
    queue_list = []
    try:
        CLIENT = boto3.client('sqs', config=REGION_CONFIG)
        response = CLIENT.list_queues()
        if not 'QueueUrls' in response:
            return (queue_list)
        else:
            ic(response['QueueUrls'])
            for queue in response['QueueUrls']:
            #desc = re.search('queue.amazonaws.com/(.*)', queue)
                queue_list.append(queue)
            return queue_list
    except Exception as e:
        return(e)
        
#Post a message to a queue 
def send_message(msg, REGION_NAME, queue_url):
    REGION_CONFIG = Config(
    region_name = REGION_NAME,
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
        }
    )
    CLIENT = boto3.client('sqs', config=REGION_CONFIG)
    message = {"test": msg}
    
    ic(message)
    
    response = CLIENT.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )
    return response

#get all the AWS regions
def get_az():
    s = Session()
    sqs_region = s.get_available_regions('sqs')
    return (sqs_region)

#---------------- Threading functions--------------------------------------
#Use thread to post messages
def msg_worker_thread(msg,region_name,queue_name,run_freq,delay, window):
    try:
        window.write_event_value('-WRITE-',"***Starting Sending Message To Queue: {}***".format(queue_name))
        for i in range(run_freq):
            resp = send_message(msg,region_name,queue_name)
            window.write_event_value('-WRITE-',resp)
            time.sleep(delay)
        window.write_event_value('-WRITE-',"***Finished Sending Message To Queue: {}***".format(queue_name))
    except Exception as e:
        window.write_event_value('-WRITE-',e)



#-----------------Main function------------------------------------
def main():
    
    window = sg.Window('SQS PLAYA', tabgrp) #layout
    
    REGION_NAME=[]
    region_loop = False
    text=""
    while True: # The Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
        if event == 'List Regions':
            try:
                if region_loop == False: #don't refresh list everytime
                    region_list = get_az()
                    window["-REGION-"].update(region_list)
                    region_loop = True
            except Exception as e:
                text  = window["-CONSOLEMSG-"]
                window["-CONSOLEMSG-"].update(text.get()+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(e))
        
        if event == 'List Queues':
            try:
                REGION_NAME=values['-REGION-'][0]
                window["-QUEUENAME-"].update([])
                url = get_queue_url(REGION_NAME)
                if not url:
                    text = window["-CONSOLEMSG-"]
                    window["-CONSOLEMSG-"].update(text.get()+ str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ": No Queues in this region")
                else:
                    window["-QUEUENAME-"].update(url)
            except Exception as e:
                text  = window["-CONSOLEMSG-"]
                window["-CONSOLEMSG-"].update(text.get()+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(e))
        
        if event == '-QUEUENAME-':
            window.find_element("-QUEUEMSG-").Update(disabled=False)        
        
        if event == '-WRITE-':
            text  = window["-CONSOLEMSG-"]
            window["-CONSOLEMSG-"].update(text.get()+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(values['-WRITE-']))
            #window.refresh
        
        if event == 'Load':
            filename = values['-INPUT-']
            if Path(filename).is_file():
                try:
                    with open(filename, "rt", encoding='utf-8') as f:
                        text = f.read()
                        window["-QUEUEMSG-"].update(text)
                except Exception as e:
                    text  = window["-CONSOLEMSG-"]
                    window["-CONSOLEMSG-"].update(text.get()+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(e))
        if event == 'Send Msg':
            try:
                counter = int(values['-ITERATE-'])
                delay = int(values['-DELAY-'])
                threading.Thread(target=msg_worker_thread, 
                                 args=(values['-QUEUEMSG-'],
                                       REGION_NAME,values["-QUEUENAME-"][0], 
                                       counter,delay, window,),  daemon=True).start()
            except Exception as e:
                text  = window["-CONSOLEMSG-"]
                window["-CONSOLEMSG-"].update(text.get()+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(e))
        
        if event == 'Run Once':
            try:
                threading.Thread(target=msg_worker_thread, 
                                 args=(values['-QUEUEMSG-'],
                                       REGION_NAME,values["-QUEUENAME-"][0], 
                                       1,0, window,),  daemon=True).start()
            except Exception as e:
                text  = window["-CONSOLEMSG-"]
                window["-CONSOLEMSG-"].update(text.get()+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(e))

        if event == 'Save Output':
            try:
                file= open("output.txt", 'a+')
            except FileNotFoundError:
                file= open("output.txt", 'w+')
            file.write(str(window["-CONSOLEMSG-"].get()))
            file.close()
            sg.popup("File Saved")
    window.close()

if __name__ == '__main__':
    main()
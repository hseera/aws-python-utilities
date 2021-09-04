# sqs_workbench.py
'''
Useful for sending one or multiple messages to AWS SQS.Especially useful for those using Windows OS.
The application is build using PySimpleGUI. 
It expects you have setup the aws id/key in
  Linux:   /home/[username]/.aws
  Windows: /Users/[username]/.aws
If you don't have aws id/key setup in the above location, you can enter those detail in the config tab. Plus your default region. 


'''

import PySimpleGUI as sg
import boto3
from botocore.config import Config
import json
from boto3.session import Session
import threading
from pathlib import Path
import datetime
import time

session = boto3.session.Session()

data=[]
sg.theme('Reddit')

#-----------------GUI Layout--------------------------------    
Region = [
         [sg.Text("Region Name (Select Region)")],
         [sg.Listbox(values=[],enable_events=True,size=(30, 8), key="-REGION-")], 
         [sg.B("List Regions",size=(13, 1)), sg.B("List Queues",size=(13, 1))]
    ]

Queue_list =[
    [sg.Text("Queue List (Select Queue from the list)")],
    [sg.Listbox(values=[], enable_events=True, size=(112, 5), key="-QUEUENAME-")],
    [sg.Table(values=data,key="-TABLE-", headings=['ApproximateNumberOfMessages', 'ApproximateNumberOfMessagesNotVisible', 'ApproximateNumberOfMessagesDelayed'],auto_size_columns=False, col_widths=[27, 30, 30],  num_rows=3)]
    ]

Post_message =[
    [sg.Text("Message PayLoad")],
    [sg.Text("FilePath"),sg.Input(key='-INPUT-', size=(45, 1)),sg.FileBrowse(file_types=(("Json Files", "*.json"),),size=(10, 1)),sg.B("Load",size=(10, 1))],
    [sg.Multiline(size=(80, 18),key="-QUEUEMSG-")],
    [sg.Text("# of Msg To Send"),sg.In(size=(5, 1),key='-ITERATE-'),
     sg.Text("Delay Btw Msgs (sec)"),sg.In(size=(5, 1),key='-DELAY-'),
     sg.B("Send Multi Msgs",size=(13, 1)),sg.B("Send Once",size=(11, 1))] #
    
    ]

Console =[
    [sg.Text("Console")],
    [sg.Multiline(size=(60, 22),key="-CONSOLEMSG-",disabled=True)],
    [sg.B("Clear Output",size=(26, 1)),sg.B("Save Output",size=(26, 1))]
    ]

Region_buttons =[
    [sg.B("List Regions",size=(12, 1)), sg.B("List Queues",size=(13, 1))]
    ]

Receive_button =[
    [sg.B("Receive Msg",size=(12, 1))]
    ]
layout3 =[
    [  
        sg.Column(Post_message)
    ]]

layout4 =[
    [sg.Column(Receive_button)],
    [sg.Multiline(size=(80, 22),key="-RECEIVEMSG-",disabled=True)]
    ]
layout = [

    [
        sg.Column(Region),
        sg.VSeperator(),
        sg.Column(Queue_list)],      
     [sg.TabGroup([[sg.Tab('Send', layout3, tooltip='Send Message To An SQS')],[
         sg.Tab('Receive', layout4, tooltip='Send Message To An SQS')]]),
        sg.VSeperator(),
        sg.Column(Console)]   
]

config =[
    [sg.Text('Enter Your AWS Id',size=(30, 1)), sg.InputText(key="-AWSID-",size=(30, 1))],
    [sg.Text('Enter Your AWS Key',size=(30, 1)), sg.InputText(key="-AWSKEY-",size=(30, 1))],
    [sg.Text('Enter Your Default Region',size=(30, 1)), sg.InputText(key="-DEFREGION-",size=(30, 1))],
    [sg.B("Reset",size=(28, 1)),sg.B("Connect",size=(27, 1))]
    ]

layout2 = [[sg.Column(config)]]

tabgrp = [[sg.TabGroup([[sg.Tab('Config', layout2)],[sg.Tab('SQS', layout)]])]]  

#--------------AWS SQS specific Functions--------------------------------------

#get list of all the available queues in a region
def get_queue_url(REGION_NAME,window):
    
    REGION_CONFIG = Config(
    region_name = REGION_NAME,
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
        }
    )
  
    queue_list = []
    try:
        CLIENT = session.client('sqs', config=REGION_CONFIG)
        response = CLIENT.list_queues()
        if not 'QueueUrls' in response:
            #window.write_event_value('-WRITE-',"***No Queues available/Check connection detail***")
            return (queue_list)
        else:
            for queue in response['QueueUrls']:
            #desc = re.search('queue.amazonaws.com/(.*)', queue)
                queue_list.append(queue)
            return queue_list
    except Exception as e:
        return(e)

def get_queue_attrib(REGION_NAME, queue_url):
    REGION_CONFIG = Config(
    region_name = REGION_NAME,
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
        }
    )
    CLIENT = session.client('sqs', config=REGION_CONFIG)
    response = CLIENT.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['All']
    )
    return response
        
#Post a message to a queue 
def send_message(msg, REGION_NAME, queue_url):
    REGION_CONFIG = Config(
    region_name = REGION_NAME,
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
        }
    )
    CLIENT = session.client('sqs', config=REGION_CONFIG)
    #message = {"test": msg}    
    response = CLIENT.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(msg)
    )
    return response

def receive_message(REGION_NAME, queue_url):
    REGION_CONFIG = Config(
    region_name = REGION_NAME,
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
        }
    )
    CLIENT = session.client('sqs', config=REGION_CONFIG)
    
    response = CLIENT.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['ALL']
    )
    return response


#get all the AWS regions
def get_az():
    #s = Session()
    sqs_region = session.get_available_regions('sqs')
    return (sqs_region)

#---------------- Threading functions--------------------------------------
#Use thread to post messages
def msg_worker_thread(msg,region_name,queue_name,run_freq,delay, window):
    try:
        window.write_event_value('-WRITE-',"***Starting Sending Message To Queue: {}***".format(queue_name))
        for i in range(run_freq):
            start_timer = time.perf_counter()
            resp = send_message(msg,region_name,queue_name)
            end_timer =time.perf_counter()
            window.write_event_value('-WRITE-',resp)
            window.write_event_value('-WRITE-',"Execution Time (sec): {}".format(end_timer - start_timer))
            time.sleep(delay)
        window.write_event_value('-WRITE-',"***Finished Sending Message To Queue: {}***".format(queue_name))
    except Exception as e:
        window.write_event_value('-WRITE-',e)


def msg_worker_thread1(region_name,queue_name,run_freq,delay, window):
    try:
        window.write_event_value('-WRITE-',"***Starting Receving Message To Queue: {}***".format(queue_name))
        for i in range(run_freq):
            start_timer = time.perf_counter()
            resp = receive_message(region_name,queue_name)
            end_timer =time.perf_counter()
            window.write_event_value('-RECEIVE-',resp['Messages'][0]['Body'])
            window.write_event_value('-WRITE-',resp['ResponseMetadata'])
            window.write_event_value('-WRITE-',"Execution Time (sec): {}".format(end_timer - start_timer))
            time.sleep(delay)
        window.write_event_value('-WRITE-',"***Finished Receiving Message To Queue: {}***".format(queue_name))
    except Exception as e:
        window.write_event_value('-WRITE-',e)


#-----------------Main function------------------------------------
def main():
    
    window = sg.Window('AWS SQS WORKBENCH', tabgrp) #layout
    
    REGION_NAME=[]
    region_loop = False
    text=""
    while True: # The Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        #---------Connection Tab-----------------------------
        if event == 'Reset':
            try:
                window["-AWSID-"].update("")
                window["-AWSKEY-"].update("")
                window["-DEFREGION-"].update("")
                window["-AWSID-"].SetFocus(force = True)
            except Exception as e:
                sg.popup(e)
        
        if event == 'Connect':
            try:
                global session
                
                if values['-DEFREGION-'] == "":
                    sg.popup("Region Field is missing")
                elif values['-AWSID-'] == "":
                    sg.popup("AWS ID Field is missing")
                elif values['-AWSKEY-'] == "":
                    sg.popup("AWS KEY Field is missing")
                else:
                    session = Session(region_name=values['-DEFREGION-'], aws_access_key_id=values['-AWSID-'],
                                  aws_secret_access_key=values['-AWSKEY-'])
                #print(session.get_credentials().access_key)
                #print(session.get_credentials().secret_key)
                #print(session.region_name)
            except Exception as e:
                sg.popup(e)
        
        #---------Send SQS Message Tab------------------------
        if event == 'List Regions':
            try:
                if region_loop == False: #don't refresh list everytime
                    region_list = get_az()
                    window["-REGION-"].update(region_list)
                    region_loop = True
            except Exception as e:
                window["-CONSOLEMSG-"].update(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(e)+"\n", append=True )
        
        if event == 'List Queues':
            try:
                REGION_NAME=values['-REGION-'][0]
                window["-QUEUENAME-"].update([])
                url = get_queue_url(REGION_NAME,window)
                if not url:
                    data=[]
                    window["-TABLE-"].update(data)
                    window["-CONSOLEMSG-"].update(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ": No Queues in this region\n", append=True)
                else:
                    window["-QUEUENAME-"].update(url)
            except Exception as e:
                window["-CONSOLEMSG-"].update(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(e) +" /Check Connection Detail\n", append=True)
        
        if event == '-QUEUENAME-':
            try:
                REGION_NAME=values['-REGION-'][0]
                window.find_element("-QUEUEMSG-").Update(disabled=False)
                #window.find_element("-TABLE-").Update(disabled=False)
                data=[]
                resp = get_queue_attrib(REGION_NAME, values['-QUEUENAME-'][0])
                data.append([resp['Attributes']['ApproximateNumberOfMessages'],
                             resp['Attributes']['ApproximateNumberOfMessagesNotVisible'],
                             resp['Attributes']['ApproximateNumberOfMessagesDelayed']])
                window["-TABLE-"].update(data)
            except Exception as e:
                window["-CONSOLEMSG-"].update(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(e)+"\n", append=True)
        
        if event == '-RECEIVE-':
            window['-RECEIVEMSG-'].update(str(values['-RECEIVE-']))
            
        if event == '-WRITE-':
            window["-CONSOLEMSG-"].update(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(values['-WRITE-'])+"\n", append=True)
            #window.refresh
        
        if event == 'Load':
            filename = values['-INPUT-']
            if Path(filename).is_file():
                try:
                    with open(filename, "rt", encoding='utf-8') as f:
                        text = f.read()
                        window["-QUEUEMSG-"].update(text)
                except Exception as e:
                    window["-CONSOLEMSG-"].update(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(e)+"\n", append=True)
        if event == 'Send Multi Msgs':
            try:
                counter = int(values['-ITERATE-'])
                delay = int(values['-DELAY-'])
                threading.Thread(target=msg_worker_thread, 
                                 args=(values['-QUEUEMSG-'],
                                       REGION_NAME,values["-QUEUENAME-"][0], 
                                       counter,delay, window,),  daemon=True).start()
            except Exception as e:
                window["-CONSOLEMSG-"].update(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(e)+"\n", append=True)
        
        if event == 'Send Once':
            try:
                threading.Thread(target=msg_worker_thread, 
                                 args=(values['-QUEUEMSG-'],
                                       REGION_NAME,values["-QUEUENAME-"][0], 
                                       1,0, window,),  daemon=True).start()
            except Exception as e:
                window["-CONSOLEMSG-"].update(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(e)+"\n", append=True)

        
        if event == 'Receive Msg':
            try:
                threading.Thread(target=msg_worker_thread1, 
                                 args=(REGION_NAME,values["-QUEUENAME-"][0], 
                                       1,0, window,),  daemon=True).start()
            except Exception as e:
                window["-CONSOLEMSG-"].update(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +": "+str(e)+"\n", append=True)
            
        if event == 'Save Output':
            try:
                file= open("output.txt", 'a+')
            except FileNotFoundError:
                file= open("output.txt", 'w+')
            file.write(str(window["-CONSOLEMSG-"].get()))
            file.close()
            sg.popup("File Saved")
        
        
        if event == 'Clear Output':
            window["-CONSOLEMSG-"].update("")
    window.close()

if __name__ == '__main__':
    main()

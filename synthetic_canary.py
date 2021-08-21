# -*- coding: utf-8 -*-
"""
To stop or start all canaries:
    cmd: ./start_stop_all_canaries.py stop/start
    example: 
        ./synthetic_canary.py stop
        ./synthetic_canary.py start

To stop or start a canary:
    cmd: ./synthetic_canary.py stop/start {canary name}
    example: 
        ./synthetic_canary.py stop workload
        ./synthetic_canary.py start workload

To delete a canary:
    cmd: ./synthetic_canary.py delete {canary name}
    example: 
        ./synthetic_canary.py delete workload

To create a canary:
    cmd: ./synthetic_canary.py create {canary name}
    example: 
        ./synthetic_canary.py create workload
    NOTE: 
        1: The create canary script doesn't include vpc,tag or env info in the payload. 
        Pass those in the payload if they are important for your usecase.
        2: Your python zip file needs to be in the following folder structure when you load to s3
           .zip
           ->python/
           --->file.py
        3: Your nodejs zip file needs to be in the following folder structure when you load to s3
           .zip
           ->nodejs/
           --->node_modules/
           ------>file.py


TO DO:
    1. Currently describe only returns 20 canaries. Update the code to get all.
"""

import boto3
from botocore.config import Config
from pandas import DataFrame
import sys
import time

#Update the region config based on your usecase
REGION_CONFIG = Config(
    region_name = 'ap-southeast-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
    }
)

CLIENT = boto3.client('synthetics', config=REGION_CONFIG)


#Create canary variables.
S3BUCKET = 'xxxx' #s3 bucket name where script is located
S3KEY = 'xxxx.zip' #script/key name. Make sure it is zipped
SCRIPT_HANDLER = 'xxxx.handler' #script handler name
ARTIFACTS3LOCATION = 'xxxx' #S3 location where canary artiacts need to be saved
EXECUTIONROLEARN = 'xxxx' #ExecutionRoleArn
SCRIPTRUNTIMEVERSION = 'xxxx' #nodejs/python script runtime version. i.e current python script runtime version is syn-python-selenium-1.0


def describe_canaries():
    canary_info = []
    try:
        response = CLIENT.describe_canaries(
            MaxResults=20
            )
        for canaries in response['Canaries']:
            canary_info.append((canaries['Name'],canaries['Status']['State']))
        return canary_info
    except Exception as e:
        print(e)



#Start stop all canaries
def start_stop_all_canaries(option):
    try:
        canary_info = describe_canaries()
        df = DataFrame(canary_info,columns=['Name','State'])
        if option =="stop":
            get_canary_list = (df.loc[df['State'] == 'RUNNING'])['Name'].values.tolist()
            
            if not get_canary_list: #Check for empty list
                print("Canaries are already in a stop state")
            else:
                for canary in get_canary_list:
                    response = CLIENT.stop_canary(
                        Name=canary
                        )
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print("Stopping {} canary".format(canary))
                    else:
                        print("Stopping {} canary was not successful".format(canary))
                        
        elif option =="start":
            get_canary_list = (df.loc[(df['State'] == 'STOPPED') | (df['State'] == 'READY')])['Name'].values.tolist()
            if not get_canary_list: #Check for empty list
                print("None of the canaries in a stop state")
            else:
                for canary in get_canary_list:
                    response = CLIENT.start_canary(
                        Name=canary
                        )
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print("Starting {} canary".format(canary))
                    else:
                        print("Starting {} canary was not successful".format(canary))
        else:
            print("Unrecognized option")
    except Exception as e:
        print(e)

def start_stop_a_canary(option, canary_name):
    try:
        canary_info = describe_canaries()
        df = DataFrame(canary_info,columns=['Name','State'])
        if option =="stop":  #stop a canary
            get_canary_list = (df.loc[df['State'] == 'RUNNING'])['Name'].values.tolist() 
            if not get_canary_list: #Check for empty list
                print("Canaries are already in a stop state")
            else:
                if canary_name in get_canary_list:
                    response = CLIENT.stop_canary(
                        Name=canary_name
                        )
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print("Stopping {} canary".format(canary_name))
                    else:
                        print("Stopping {} canary was not successful".format(canary_name))
                else:
                    print("Canary does not exist")
                    
        elif option =="start": #start a canary
            get_canary_list = (df.loc[(df['State'] == 'STOPPED') | (df['State'] == 'READY')])['Name'].values.tolist()
            if not get_canary_list: #Check for empty list
                print("None of the canaries in a stop state")
            else:
                if canary_name in get_canary_list:
                    response = CLIENT.start_canary(
                        Name=canary_name
                        )
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print("Starting {} canary".format(canary_name))
                    else:
                        print("Starting {} canary was not successful".format(canary_name))
                else:
                    print("Canary does not exist")
                    
        else:
            print("Unrecognized option")
    except Exception as e:
        print(e)

def delete_canary(option, canary_name):
    try:
        canary_info = describe_canaries()
        df = DataFrame(canary_info,columns=['Name','State'])
        get_canary_list = (df.loc[df['State'] != 'DELETEING'])['Name'].values.tolist()
        if not get_canary_list: #Check for empty list
                print("No canaries to delete")
        else:
            if canary_name in get_canary_list and option=='delete':
                response = CLIENT.delete_canary(
                        Name=canary_name
                        )
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print("Deleting {} canary".format(canary_name))
                else:
                        print("Deleting {} canary was not successful".format(canary_name))
            else:
                print("Canary is already been deleted/does not exist/wrong option")
        
    except Exception as e:
        print(e)


def create_canary(option, canary_name):
    try:
        canary_info = describe_canaries()
        df = DataFrame(canary_info,columns=['Name','State'])
        get_canary_list = df['Name'].values.tolist()
        
        if canary_name in get_canary_list:
            print("Given {} canary name already exists".format(canary_name))
        else:
            response = CLIENT.create_canary(
                    Name=canary_name,
                    Code={
                        'S3Bucket': S3BUCKET,
                        'S3Key': S3KEY,
                        'Handler': SCRIPT_HANDLER
                    },
                    ArtifactS3Location=ARTIFACTS3LOCATION,
                    ExecutionRoleArn=EXECUTIONROLEARN,
                    Schedule={
                        'Expression': 'rate(30 minutes)',
                        'DurationInSeconds': 0
                    },
                    RunConfig={
                        'TimeoutInSeconds': 120,
                        'MemoryInMB': 960,
                        'ActiveTracing': False
                    },
                    SuccessRetentionPeriodInDays=31,
                    FailureRetentionPeriodInDays=31,
                    RuntimeVersion=SCRIPTRUNTIMEVERSION,
                )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print("{} canary was successfully created".format(canary_name))
                time.sleep(20)
                start_stop_a_canary('start',canary_name)
            else:
                print("Something went wrong. {} canary was not successfully created".format(canary_name))
    
    except Exception as e:
        print(e)
        
        
        
def main(argv):
    if len(sys.argv) == 1:
        print("Please pass in the correct script arguments")
    elif len(sys.argv) == 2:
        if str(sys.argv[1])=="start" or str(sys.argv[1])=="stop":
            start_stop_all_canaries(str(sys.argv[1]))
        else:
            print("Wrong number of arguments or unrecognized arguments")
    elif len(sys.argv) == 3:
        if str(sys.argv[1])=="delete":
           delete_canary(str(sys.argv[1]),str(sys.argv[2]))
        elif str(sys.argv[1])=="start" or str(sys.argv[1])=="stop":
           start_stop_a_canary(str(sys.argv[1]),str(sys.argv[2]))
        elif str(sys.argv[1])=="create":
           create_canary(str(sys.argv[1]),str(sys.argv[2]))
        else:
            print("Wrong number of arguments or unrecognized arguments")
    else:
        print("Wrong number of arguments or unrecognized arguments")


if __name__ == "__main__":
    main(sys.argv)

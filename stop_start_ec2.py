# -*- coding: utf-8 -*-
"""
To stop or start all instances:
    cmd: ./stop_start_ec2.py stop/start id

To stop or start all instances by instance type:
    cmd: ./stop_start_ec2.py stop/start type {instance type}
    example: ./stop_start_ec2.py stop/start type t2.micro

To stop or start all instances by platform (i.e. windows or other):
    cmd: ./stop_start_ec2.py stop/start platform {platform}
    example: ./stop_start_ec2.py {stop/start} platform {windows/other}

TO DO:
    1. Terminate instances
    2. Stop/start given instance id
    3. Stop/start by tag
"""

import boto3
from botocore.config import Config
from pandas import DataFrame
import sys
import pandas as pd

REGION_CONFIG = Config(
    region_name = 'ap-southeast-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
    }
)

CLIENT = boto3.client('ec2', config=REGION_CONFIG)

#descript all ec2 instance and extract instanceid, instancetype, state-name, state-code,platform info.
def describe_ec2():
    ec2_info = []
    try:
        response = CLIENT.describe_instances(
                DryRun=False,
                MaxResults=123)
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if 'Platform' in instance:
                    ec2_info.append((instance['InstanceId'],instance['InstanceType'],instance['State']['Code'],instance['State']['Name'],instance['Platform']))
                else:
                    ec2_info.append((instance['InstanceId'],instance['InstanceType'],instance['State']['Code'],instance['State']['Name'],"other"))    
        
        return ec2_info
    except Exception as e:
        print(e)

#stop/start all instances
def instanceid(option):
    try:
        ec2_info = describe_ec2()
        df = DataFrame(ec2_info,columns=['InstanceId','InstanceType','State-Code','State-Name','Platform'])
        if option =="stop":
            get_ec2_list = df.loc[df['State-Name'] == 'running']
            instance_id = get_ec2_list['InstanceId'].values.tolist()
            response = CLIENT.stop_instances(
                    InstanceIds= instance_id,
                    DryRun=False,
                    Force=False
                    )
            print(response)
        elif option =="start":
            get_ec2_list = df.loc[df['State-Name'] == 'stopped']
            instance_id = get_ec2_list['InstanceId'].values.tolist()
            response = CLIENT.start_instances(
                    InstanceIds= instance_id,
                    DryRun=False
                    )
            print(response)
        else:
            print("unrecognized option")
    except Exception as e:
        print(e)

#stop/start instances by given instance type
def instance_type(option, instancetype):
    try:
        ec2_info = describe_ec2()
        df = DataFrame(ec2_info,columns=['InstanceId','InstanceType','State-Code','State-Name','Platform'])
        if option == "stop":
            get_ec2_list = df.loc[(df['InstanceType'] == instancetype) & (df['State-Name']=='running')]
            instance_id = get_ec2_list['InstanceId'].values.tolist()
            response = CLIENT.stop_instances(
                    InstanceIds= instance_id,
                    DryRun=False,
                    Force=False
                    )
            print(response)
        elif option == "start":
            get_ec2_list = df.loc[(df['InstanceType'] == instancetype) & (df['State-Name']=='stopped')]
            instance_id = get_ec2_list['InstanceId'].values.tolist()
            response = CLIENT.start_instances(
                    InstanceIds= instance_id,
                    DryRun=False
                    )
            print(response)
        else:
            print("unrecognized option")
    except Exception as e:
        print(e)

  
#stop/start instance by given platform type  
def platform(option, platform):
    try:
        ec2_info = describe_ec2()
        df = DataFrame(ec2_info,columns=['InstanceId','InstanceType','State-Code','State-Name','Platform'])
        if option =="stop":
            get_ec2_list = df.loc[(df['Platform'] == platform) & (df['State-Name']=='running')]
            instance_id = get_ec2_list['InstanceId'].values.tolist()
            response = CLIENT.stop_instances(
                    InstanceIds= instance_id,
                    DryRun=False,
                    Force=False
                    )
            print(response)
        elif option =="start":
            get_ec2_list = df.loc[(df['Platform'] == platform) & (df['State-Name']=='stopped')]
            instance_id = get_ec2_list['InstanceId'].values.tolist()
            response = CLIENT.start_instances(
                    InstanceIds= instance_id,
                    DryRun=False
                    )
            print(response)
        else:
            print("unrecognized option")
    except Exception as e:
        print(e)
    
    
def main(argv):
    if len(sys.argv) == 1:
        print("Please pass in the argument and their values")
    elif len(sys.argv) == 2:
        print("Please pass in the argument and their values")
    elif len(sys.argv) == 3:
        if str(sys.argv[2])=="id":
            instanceid(str(sys.argv[1]))
    elif len(sys.argv) == 4:
        if str(sys.argv[2]) == "type":
            instance_type(str(sys.argv[1]),str(sys.argv[3]))
        if str(sys.argv[2]) == "platform":
            platform(str(sys.argv[1]),str(sys.argv[3]))
    else:
        print("wrong number of parameters")



if __name__ == "__main__":
    main(sys.argv)
# -*- coding: utf-8 -*-
"""

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
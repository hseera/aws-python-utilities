# -*- coding: utf-8 -*-
import boto3
import time
from botocore.config import Config
import random
import pandas as pd

FILE_TO_READ ="./Data/query-scan.csv"  # Replace with your data file

RESULT_FILE ="./Data/result-query-scan.csv" #Replace where the result needs to be saved

MAX_RANGE_VALUE = 10 #Max iteration value

#Set region config. It will overwrite region setting done as part of aws access key setup.
REGION_CONFIG = Config(
    region_name = 'ap-southeast-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
    }
)

dynamodb_client = boto3.client('dynamodb', config=REGION_CONFIG)

df1 = pd.DataFrame(columns=['Query'])
df2 = pd.DataFrame(columns=['Scan'])

'''
Perform query calls. Pass in random data from the file as a parameter.
Execute query calls equal to MAX_RANGE_VALUE.
The query call will continue to loop while response has 'LastEvaluatedKey'.
'''
for i in range(0, MAX_RANGE_VALUE):

    random_lines = random.choice(open(FILE_TO_READ).readlines())
    
    #Pass parameter values based on your dynamodb table information. Also update the parameter values in while loop too.
    operation_parameters = {
      'TableName': 'workload',
      'ExpressionAttributeNames':{ "#dyno_uuid": "uuid" },
      'KeyConditionExpression': '#dyno_uuid = :uuid_2',
      'ExpressionAttributeValues': {
         ':uuid_2': {'S': random_lines.strip()}
      }
    }
    
    start_timer = time.perf_counter()
    response = dynamodb_client.query(**operation_parameters)
    
    while ('LastEvaluatedKey' in response):
        response = dynamodb_client.query(
                  TableName= 'workload',
                  Select= 'ALL_ATTRIBUTES',
                  ExpressionAttributeNames={ "#dyno_uuid": "uuid" },
                  KeyConditionExpression= '#dyno_uuid = :uuid_2',
                  ExpressionAttributeValues= {
                     ':uuid_2': {'S': random_lines.strip()}
                  },
                  ExclusiveStartKey=response['LastEvaluatedKey']
                ) 
    end_timer = time.perf_counter()
    #print("%s-%s-%s" %(response['Count'],response['ResponseMetadata']['HTTPHeaders']['content-length'],response['Items'][0]['uuid']))   
    df1 = df1.append({'Query': end_timer-start_timer}, ignore_index=True)


'''
Perform scan calls. Pass in random data from the file as a parameter.
Execute scan calls equal to MAX_RANGE_VALUE.
The scan call will continue to scan data until it finds it. 
It uses 'LastEvaluatedKey' & empty response to check the condition to continue scanning the table. 
'''
for i in range(0, MAX_RANGE_VALUE):

    random_lines = random.choice(open(FILE_TO_READ).readlines())
    
    #Pass parameter values based on your dynamodb table information. Also update the parameter values in while loop too.
    operation_parameters = {
      'TableName': 'workload',
      'Select': 'ALL_ATTRIBUTES',
      'ExpressionAttributeNames':{ "#dyno_uuid": "uuid" },
      'FilterExpression': '#dyno_uuid = :uuid_2',
      'ExpressionAttributeValues': {
         ':uuid_2': {'S': random_lines.strip()}
      }
    }

    start_timer = time.perf_counter()
    response = dynamodb_client.scan(**operation_parameters)
    while ('LastEvaluatedKey' in response and response['Items']==[]):
        response = dynamodb_client.scan(
                  TableName= 'workload',
                  Select= 'ALL_ATTRIBUTES',
                  ExpressionAttributeNames={ "#dyno_uuid": "uuid" },
                  FilterExpression= '#dyno_uuid = :uuid_2',
                  ExpressionAttributeValues= {
                     ':uuid_2': {'S': random_lines.strip()}
                  },
                  ExclusiveStartKey=response['LastEvaluatedKey']
                )
    end_timer = time.perf_counter()
    #print("%s-%s-%s" %(response['Count'],response['ResponseMetadata']['HTTPHeaders']['content-length'],response['Items'][0]['uuid']))   
    df2 = df2.append({'Scan': end_timer-start_timer}, ignore_index=True)

df_col_merged = pd.concat([df1, df2], axis=1)

print(df_col_merged.describe(percentiles=[0.25,0.5,0.75,0.90,0.95],include='all'))

df_col_merged.to_csv(RESULT_FILE,index=False)

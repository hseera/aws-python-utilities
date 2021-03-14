# -*- coding: utf-8 -*-
import boto3
import time
from botocore.config import Config
import random
import pandas as pd


MAX_RANGE_VALUE = 350 #Max iteration value

#Set region config. It will overwrite region setting done as part of aws access key setup.
REGION_CONFIG = Config(
    region_name = 'ap-southeast-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
    }
)


#Execute batch_get_item dynamodb call    
def batch_get_item(FILE_TO_READ,REGION_CONFIG):
    df2 = pd.DataFrame(columns=['batch_get_item'])
    dynamodb_client = boto3.client('dynamodb', config=REGION_CONFIG) 
    for i in range(0, MAX_RANGE_VALUE):
        random_lines = random.choice(open(FILE_TO_READ).readlines())
        start_timer = time.perf_counter()
        response = dynamodb_client.batch_get_item(RequestItems={'workload':
            {'Keys': [{'uuid': {'S': random_lines.strip()}}]}})
        end_timer = time.perf_counter()
        print("%s:-:%s" %(response['ResponseMetadata']['HTTPHeaders']['content-length'],response['Responses']['workload'][0]['uuid'])) #print the response size and uuid is in response
        df2 = df2.append({'batch_get_item': end_timer-start_timer}, ignore_index=True)
    return df2


#Execute get_item dynamodb call   
def get_item(FILE_TO_READ,REGION_CONFIG):
    df1 = pd.DataFrame(columns=['get_item'])
    dynamodb = boto3.resource('dynamodb', config=REGION_CONFIG)
    table = dynamodb.Table('workload')
    for i in range(0, MAX_RANGE_VALUE):
        random_lines = random.choice(open(FILE_TO_READ).readlines())
        start_timer = time.perf_counter()
        response = table.get_item(Key={'uuid': random_lines.strip()})
        end_timer = time.perf_counter()
        print("%s:-:%s" %(response['ResponseMetadata']['HTTPHeaders']['content-length'],response['Item']['uuid'])) #print the response size and uuid is in response
        df1 = df1.append({'get_item': end_timer-start_timer}, ignore_index=True)
    return df1


def main():
    FILE_TO_READ ='./getItem-batchGetItem-data.csv'  # Replace with your data file
    RESULT_FILE ="./result-getItem-batchGetItem.csv" #Replace where the result needs to be saved
    df1 = get_item(FILE_TO_READ,REGION_CONFIG)
    df2 = batch_get_item(FILE_TO_READ,REGION_CONFIG)
    df_col_merged = pd.concat([df1, df2], axis=1)
    print(df_col_merged.describe(percentiles=[0.25,0.5,0.75,0.90,0.95],include='all'))
    df_col_merged.to_csv(RESULT_FILE,index=False)

    
if __name__ == "__main__":
    main()
    
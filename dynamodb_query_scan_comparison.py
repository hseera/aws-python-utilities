# -*- coding: utf-8 -*-
import boto3
import time
from botocore.config import Config
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import numpy as np

FILE_TO_READ ="./Data/query-scan.csv"  # Replace with your data file

RESULT_FILE ="./Data/result-query-scan.csv" #Replace where the result needs to be saved

MAX_RANGE_VALUE = 450 #Max iteration value

#Set region config. It will overwrite region setting done as part of aws access key setup.
REGION_CONFIG = Config(
    region_name = 'ap-southeast-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
    }
)


def run_query_and_scan_test():
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
        
        '''
        Pass parameter values based on your dynamodb table information. Also update the parameter values in while loop too.
        Using ExpressionAttrbiuteName because uuid is a reserved word in DynamoDB. And partition key of the demo table used for testing is uuid.
        '''
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
        
        '''
        Pass parameter values based on your dynamodb table information. Also update the parameter values in while loop too.
        Using ExpressionAttrbiuteName because uuid is a reserved word in DynamoDB. And partition key of the demo table used for testing is uuid.
        '''
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
    
    print(df_col_merged.describe(percentiles=[0.25,0.5,0.75,0.90,0.95, 0.99],include='all'))
    
    df_col_merged.to_csv(RESULT_FILE,index=False)


def generate_stats_graph():

    df = pd.read_csv(RESULT_FILE)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=False)
    
    kwargs = dict(element='step',shrink=.8, alpha=0.6, fill=True, legend=True) 
    ax = sns.histplot(ax=axes[0],data=df,**kwargs)
    ax.set(xlim=(0.00,1.00))
    ax.set_title('Response Time Distribution')
    ax.set_xlabel('Response Time (s)')
    ax.set_ylabel('Request Count')
    
    
    
    #generate percentile distribution       
    summary = np.round(df.describe(percentiles=[0.0, 0.1, 0.2,
                                                     0.3, 0.4, 0.5,
                                                     0.6, 0.7, 0.8,  
                                                     0.9, 0.95, 0.99, 1]),2) # add 1 in the percentile
    dropping = ['count', 'mean', 'std', 'min','max'] #remove metrics not needed for percentile graph
    
    for drop in dropping:
        summary = summary.drop(drop)
    ax = sns.lineplot(ax=axes[1],data=summary,dashes=False, legend=True)
    ax.legend(fontsize='medium')
    ax.set(ylim=(0,1))
    ax.set_title('Percentile Distribution')
    ax.set_xlabel('Percentile')
    ax.set_ylabel('Response Time (s)')
    
    fig.tight_layout(pad=1)


def main():
    run_query_and_scan_test()
    generate_stats_graph()
    

if __name__ == "__main__":
    main()
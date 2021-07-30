# -*- coding: utf-8 -*-
import boto3
import time
from botocore.config import Config
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


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
    df = pd.DataFrame(columns=['batch_get_item'])
    dynamodb_client = boto3.client('dynamodb', config=REGION_CONFIG) 
    for i in range(0, MAX_RANGE_VALUE):
        random_lines = random.choice(open(FILE_TO_READ).readlines())
        start_timer = time.perf_counter()
        response = dynamodb_client.batch_get_item(RequestItems={'workload':
            {'Keys': [{'uuid': {'S': random_lines.strip()}}]}})
        end_timer = time.perf_counter()
        #print("%s:-:%s" %(response['ResponseMetadata']['HTTPHeaders']['content-length'],response['Responses']['workload'][0]['uuid'])) #print the response size and uuid is in response to validate the response
        df = df.append({'batch_get_item': end_timer-start_timer}, ignore_index=True)
    return df


#Execute get_item dynamodb call   
def get_item(FILE_TO_READ,REGION_CONFIG):
    df = pd.DataFrame(columns=['get_item'])
    dynamodb = boto3.resource('dynamodb', config=REGION_CONFIG)
    table = dynamodb.Table('workload')
    for i in range(0, MAX_RANGE_VALUE):
        random_lines = random.choice(open(FILE_TO_READ).readlines())
        start_timer = time.perf_counter()
        response = table.get_item(Key={'uuid': random_lines.strip()})
        end_timer = time.perf_counter()
        #print("%s:-:%s" %(response['ResponseMetadata']['HTTPHeaders']['content-length'],response['Item']['uuid'])) #print the response size and uuid is in response to validate the response
        df = df.append({'get_item': end_timer-start_timer}, ignore_index=True)
    return df


def generate_stats_graph(RESULT_FILE):

    df = pd.read_csv(RESULT_FILE)
    
        
    fig, axes = plt.subplots(2, 2, figsize=(12, 10), sharey=False)
    
    #generate response time distribution
    kwargs = dict(element='step',shrink=.8, alpha=0.6, fill=True, legend=True) 
    ax = sns.histplot(ax=axes[0,0],data=df,**kwargs)
    #ax.set(xlim=(0.00,1.00)) #set the ylim boundary if auto option is not what you need
    ax.set_title('Response Time Distribution')
    ax.set_xlabel('Response Time (s)')
    ax.set_ylabel('Request Count')
    
    
    #Response Time Distribution using boxplot
    ax = sns.boxplot(ax=axes[0,1], data=df)
    #ax.legend(fontsize='medium')
    #ax.set(ylim=(0.0,1.0)) #set the ylim boundary if auto option is not what you need
    ax.set_title('Response Time Distribution')
    ax.set_xlabel('Operaiton Type')
    ax.set_ylabel('Response Time (s)')
    
    
    #generate percentile distribution       
    summary = np.round(df.describe(percentiles=[0, 0.1, 0.2,
                                                     0.3, 0.4, 0.5,
                                                     0.6, 0.7, 0.8,  
                                                     0.9, 0.95, 0.99, 1],include='all'),2) # show basic statistics as in row
    stats_summary = summary.copy()
    dropping = ['count', 'mean', 'std', 'min','max'] #remove metrics not needed for percentile graph
    
    for drop in dropping:
        summary = summary.drop(drop)
    ax = sns.lineplot(ax=axes[1,0],data=summary,dashes=False, legend=True)
    ax.legend(fontsize='medium')
    #ax.set(ylim=(0.0,1.0)) #set the ylim boundary if auto option is not what you need
    ax.set_title('Percentile Distribution')
    ax.set_xlabel('Percentile')
    ax.set_ylabel('Response Time (s)')
    
    
    #generate latency/response time basic statistics 
    axes[1, 1].axis("off")
    dropping = ['0%','100%']
    for drop in dropping:
        stats_summary = stats_summary.drop(drop)    
    table_result = axes[1, 1].table(cellText=stats_summary.values,
              rowLabels=stats_summary.index,
              colLabels=stats_summary.columns,
              cellLoc = 'right', rowLoc = 'center',
              loc='upper left')
    table_result.auto_set_font_size(False)
    table_result.set_fontsize(9)
    axes[1, 1].set_title('Response Time Statistics')
    fig.tight_layout(pad=1)

    

def main():
    FILE_TO_READ ='./Data/testdata.csv'  # Replace with your test data file
    RESULT_FILE ="./Data/result-getItem-batchGetItem.csv" #Replace where the result needs to be saved
    df_get = get_item(FILE_TO_READ,REGION_CONFIG)
    df_batch = batch_get_item(FILE_TO_READ,REGION_CONFIG)
    df_col_merged = pd.concat([df_get, df_batch], axis=1)
    #print(df_col_merged.describe(percentiles=[0.25,0.5,0.75,0.90,0.95],include='all'))
    df_col_merged.to_csv(RESULT_FILE,index=False)
    generate_stats_graph(RESULT_FILE)

    
if __name__ == "__main__":
    main()
    

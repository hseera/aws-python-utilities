# -*- coding: utf-8 -*-
import boto3
from botocore.config import Config
import json
import os
import sys
from pathlib import Path


UPLOAD_FILE="upload_data.json" #local file name where data for backup is saved before loading to S3
BACKUP_TABLE_NAME="workload" #dynamodb backup table name
LOAD_TO_TABLE_NAME ="test" #dynamodb table where data needs to be uploaded
BUCKET_NAME="my-simple-website" #s3 bucket name
KEY_NAME="dynamodb_table_backup.json" #backup data json filename in S3

#Set region config. It will overwrite region setting done as part of aws access key setup.
REGION_CONFIG = Config(
    region_name = 'ap-southeast-2',
    signature_version = 's3v4',
    retries = {
        'max_attempts': 3
    }
)


def backup_table_data(table_name, bucket_name, key_name):
    try:
        dynamodb_client = boto3.client('dynamodb', config=REGION_CONFIG)
       
        result_item = []
        operation_parameters = {
          'TableName': table_name,
          'Select': 'ALL_ATTRIBUTES'
          }
        
        response = dynamodb_client.scan(**operation_parameters)
        while ('LastEvaluatedKey' in response):
            response = dynamodb_client.scan(
                      TableName= table_name,
                      Select= 'ALL_ATTRIBUTES',
                      ExclusiveStartKey=response['LastEvaluatedKey']
                    )
            result_item.extend(response['Items'])
        
        
        with open(UPLOAD_FILE,'a') as uploadFile:
            uploadFile.write('{\n \t"Items" :')
            uploadFile.write(json.dumps(result_item, indent=4))
            uploadFile.write('\n}')
            uploadFile.close()
        
        s3_file_name = os.path.join(Path().absolute(),UPLOAD_FILE)   
        s3_client = boto3.client('s3', config=REGION_CONFIG)
        s3_client.upload_file(s3_file_name,bucket_name,key_name)
        
        print(s3_file_name)
    except Exception, e:
        print(e)
    
    

def load_table_data(load_to_table_name, bucket_name, key_name):
    try:
        dynamodb_client = boto3.client('dynamodb', config=REGION_CONFIG)
        s3_client = boto3.client('s3', config=REGION_CONFIG)
        obj = s3_client.get_object(Bucket=bucket_name,Key=key_name)
        data = json.loads(obj['Body'].read())
        for item in data['Items']:
            dynamodb_client.put_item(TableName=load_to_table_name,Item=item)
    except Exception,e:
        print(e)
     
 
def main():
    backup_table_data(BACKUP_TABLE_NAME, BUCKET_NAME, KEY_NAME)
    load_table_data(LOAD_TO_TABLE_NAME, BUCKET_NAME, KEY_NAME)
    

    
if __name__ == "__main__":
    main()

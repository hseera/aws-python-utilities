# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 17:03:40 2021

@author: harinder
"""

import boto3
from botocore.config import Config


#Set region config. It will overwrite region setting done as part of aws access key setup.
REGION_CONFIG = Config(
    region_name = 'ap-southeast-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
    }
)

TABLE_TO_UPDATE ='workload'

def enable_dynamodb_insights():
    try:
        #Create a low-level client
        dynamodb = boto3.client('dynamodb', config=REGION_CONFIG)
        
        #List all tables in dynamodb
        awstables = dynamodb.list_tables()
        
        if len(awstables['TableNames']) == 0:
            print ("No tables in DynamoDB")
        else:
            for item in awstables['TableNames']:
                #awstables_desc= dynamodb.describe_table(TableName=item)                
                if item == TABLE_TO_UPDATE:
                    response = dynamodb.describe_contributor_insights(TableName=TABLE_TO_UPDATE) #,IndexName='string'
                    print("Current Status: %s\n" %response['ContributorInsightsStatus'])
                    if (response['ContributorInsightsStatus'] =='DISABLED'):
                        status = dynamodb.update_contributor_insights(TableName=TABLE_TO_UPDATE,ContributorInsightsAction='ENABLE') #Pass IndexName if you are using one 
                    else:
                        status = dynamodb.update_contributor_insights(TableName=TABLE_TO_UPDATE,ContributorInsightsAction='DISABLE') #Pass IndexName if you are using one
                    print("Updated Status: %s\n" %status['ContributorInsightsStatus'])
                else:
                    continue
    except Exception as ex:
        print(ex)

def main():
    enable_dynamodb_insights()

if __name__ == "__main__":
    main()

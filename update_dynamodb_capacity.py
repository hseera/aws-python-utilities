# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 17:24:42 2020

@author: harinder
"""

import boto3.dynamodb
import boto3.dynamodb.conditions
import logging


              
def updateTableCapacity():
    try:
        #Create a low-level client
        dynamodb = boto3.client('dynamodb')
        
        #List all tables in dynamodb
        awstables = dynamodb.list_tables()
        
        #Check if dynamodb has no tables
        if len(awstables['TableNames']) == 0:
            print ("No tables in DynamoDB")
        else:
            for item in awstables['TableNames']:
                  awstables_desc= dynamodb.describe_table(TableName=item)
                  #Extract value of BillingMode. To make sure KeyError is not generated for tables that don't have this key, using get(). 
                  #This is mainly for provisined capacity tables as they don't have BillingMode
                  BillingMode = awstables_desc.get("Table", {}).get("BillingModeSummary", {}).get("BillingMode")
                  if BillingMode=='PAY_PER_REQUEST':
                      print(item, "table already set to On Demand Capacity\n")
                  else:
                      status = dynamodb.update_table(TableName=item,BillingMode='PAY_PER_REQUEST')
                      print ("Updating",item,"to On Demand Capacity. Billing Status changed to ", status['TableDescription']['BillingModeSummary']['BillingMode'],"\n")
    except Exception as ex:
        logging.exception('Caught an error')
        

def main():
    updateTableCapacity()

if __name__ == "__main__":
    main()

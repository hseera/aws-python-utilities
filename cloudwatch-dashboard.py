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

#Sample cloudwatch dashboard json
DASHBOARD_JSON ='{"widgets": [{"type": "metric",\
                "x": 0,\
                "y": 0,\
                "width": 24,\
                "height": 6,\
                "properties": {\
                "metrics": [\
                            [ "AWS/Lambda", "Errors", "FunctionName", "workload", { "yAxis": "right" } ],\
                            [ ".", "Invocations", ".", "." ],\
                            [ ".", "Throttles", ".", ".", { "yAxis": "right" } ]\
                            ],\
                "view": "timeSeries",\
                "stacked": false,\
                "region": "ap-southeast-2",\
                "stat": "Average",\
                "period": 300,\
                "title": "Lambda Stats"\
                }}]}'



def create_cloudwatch_dashboard(DASHBOARD_NAME):
    try:
        #Create a low-level client
        cloudwatch = boto3.client('cloudwatch', config=REGION_CONFIG)
            
        response = cloudwatch.put_dashboard(
                DashboardName=DASHBOARD_NAME,
                DashboardBody=DASHBOARD_JSON
                )
        if 'ResponseMetadata' in response:
            print('table created successfully')
        else:
            print(response)
    except Exception as ex:
        print(ex)


def delete_cloudwatch_dashboard(DASHBOARD_NAME):
    try:
        #Create a low-level client
        cloudwatch = boto3.client('cloudwatch', config=REGION_CONFIG)
                    
        response = cloudwatch.delete_dashboards(
                DashboardNames=[DASHBOARD_NAME]
                )
        if 'ResponseMetadata' in response:
            print('table deleted successfully')
        else:
            print(response)
    except Exception as ex:
        print(ex)


def main():
    #sample dashboard name
    DASHBOARD_NAME = 'test124'
    
    #create_cloudwatch_dashboard(DASHBOARD_NAME)
    delete_cloudwatch_dashboard(DASHBOARD_NAME)

if __name__ == "__main__":
    main()

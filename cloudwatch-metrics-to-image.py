# -*- coding: utf-8 -*-

import boto3
import logging
import time
import sys
from botocore.config import Config

#Set the image path
FILEPATH='./image.png'

#Set the timezone value. Default is AEST
TIMEZONE ='+1100'

#Set region config. It will overwrite region setting done as part of aws access key setup.
REGION_CONFIG = Config(
    region_name = 'ap-southeast-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
    }
)

"""
Convert the start and end time in epoch (millisecond) to the correct format 
required by the AWS Image API Json payload below.
"""
def generate_time(start_time, end_time):
    try:
        sec_start,milli_start = divmod(int(start_time),1000)
        sec_end,milli_end = divmod(int(end_time),1000)
        start_metric_time = '{}.{:03d}Z'.format(time.strftime('%Y-%m-%dT%H:%M:%S',time.gmtime(sec_start)),milli_start)
        end_metric_time = '{}.{:03d}Z'.format(time.strftime('%Y-%m-%dT%H:%M:%S',time.gmtime(sec_end)),milli_end)
        
        return start_metric_time, end_metric_time
    except Exception as ex:
        logging.exception('Caught an error: %s' %ex)


"""
Replace the below json payload with the correct cloudwatch 
metrics payload for which you want to generate an Image.
"""
def cloudwatch_metrics_image(start_metric_time, end_metric_time):
    try:
        cloudwatch = boto3.client('cloudwatch', config=REGION_CONFIG)
           
        json='{ "view": "timeSeries",\
                "stacked": false,\
                "metrics": [\
                            [ "AWS/ApiGateway", "Latency", "ApiName", "workload_model-API", "Resource", "/workload", "Stage", "test", "Method", "GET" ],\
                            [ ".", "Count", ".", ".", ".", ".", ".", ".", ".", "." ],\
                            [ ".", "5XXError", ".", ".", ".", ".", ".", ".", ".", "." ]],\
                "width": 1100,\
                "height": 400,\
                "start":"'+start_metric_time+'",\
                "end": "'+end_metric_time+'",\
                "timezone": "'+TIMEZONE+'"\
            }'
        
        response = cloudwatch.get_metric_widget_image(MetricWidget=json)
        return response
    except Exception as ex:
        logging.exception('Caught an error')
    
    

"""
Given a start and end time in epoch (ms),generate Image for a given Cloudwatch Metrics.
"""
def generate_image(start_time, end_time):
    try:
        start_metric_time, end_metric_time = generate_time(start_time, end_time)
        response = cloudwatch_metrics_image(start_metric_time, end_metric_time)
        
        #Save binary data as png
        with open(FILEPATH,'wb') as f:
            f.write(response["MetricWidgetImage"])
        
    except Exception as ex:
        logging.exception('Caught an error')
        
        
def main(startTime, endTime):
    generate_image(startTime, endTime)

if __name__ == "__main__":
    #main(1609726800999,1609729200000)
    main(sys.argv[1],sys.argv[2])

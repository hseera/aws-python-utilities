# -*- coding: utf-8 -*-
"""
TODO:
    1: Add a progress status
    
"""

import boto3
import datetime
from botocore.config import Config
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import requests
import json

REGION_CONFIG = Config(
    region_name = 'ap-southeast-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
    }
)

RESULT_FILE ="./Data/spotInstance.csv" #Path to save the data

#replace region code with region name
REGIONS =[
    #find -> replace
    ('us-east-2','US East (Ohio)'),
    ('us-east-1','US East (N. Virginia)'),
    ('us-west-1','US West (N. California)'),
    ('us-west-2','US West (Oregon)'),
    ('af-south-1','Africa (Cape Town)'),
    ('ap-east-1','AP (Hong Kong)'),
    ('ap-south-1','AP (Mumbai)'),
    ('ap-northeast-3','AP (Osaka)'),
    ('ap-northeast-2','AP (Seoul)'),
    ('ap-southeast-1','AP (Singapore)'),
    ('ap-southeast-2','AP (Sydney)'),
    ('ap-northeast-1','AP (Tokyo)'),
    ('ca-central-1','Canada (Central)'),
    ('cn-north-1','China (Beijing)'),
    ('cn-northwest-1','China (Ningxia)'),
    ('eu-central-1','Europe (Frankfurt)'),
    ('eu-west-1','Europe (Ireland)'),
    ('eu-west-2','Europe (London)'),
    ('eu-south-1','Europe (Milan)'),
    ('eu-west-3','Europe (Paris)'),
    ('eu-north-1','Europe (Stockholm)'),
    ('me-south-1','ME (Bahrain)'),
    ('sa-east-1','SA (Sao Paulo)')
    ]

RATES =[
       (0,'<5%'),
       (1,'5-10%'),
       (2,'10-15%'),
       (3,'15-20%'),
       (4,'>20%'),
       ]

#get spot information for given instance type, region and availability zone 
def get_spot_information():
    
    try:
        client = boto3.client('ec2', config=REGION_CONFIG)
        regions = [x["RegionName"] for x in client.describe_regions()["Regions"]]
        
        '''
        Replace the instance type of your choice in the list below. 
        If you want to generate the data for all the instances in all the regions
        then replace the instance list with the following code:
            
        instances = [x["InstanceType"] for x in client.describe_instance_types()["InstanceTypes"]]
            
        '''
        instances =['t3a.small','t3a.2xlarge','c5a.large','m4.xlarge']
        
        result = []
        
        url_interruptions = "https://spot-bid-advisor.s3.amazonaws.com/spot-advisor-data.json"
        response = requests.get(url=url_interruptions)
        spot_advisor = json.loads(response.text)['spot_advisor']
        
        for instance in instances:
            for region in regions:
                client = boto3.client('ec2',region_name=region)
                Time = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
                prices = client.describe_spot_price_history(
                    InstanceTypes=[instance],
                    ProductDescriptions=['Linux/UNIX','Windows'],
                    StartTime = Time,
                    MaxResults=1
                    )
                for price in prices['SpotPriceHistory']:
                    try:
                        if (price["ProductDescription"] == "Linux/UNIX (Amazon VPC)" or price["ProductDescription"] == "Linux/UNIX"):
                            interrupt_rate = spot_advisor[region]['Linux'][instance]['r']
                        if (price["ProductDescription"] == "Windows" or price["ProductDescription"] == "Windows (Amazon VPC)"):
                            interrupt_rate = spot_advisor[region]['Windows'][instance]['r']  
                        for target, replacement in REGIONS:
                            if region == target:
                                regionName = replacement
                        for target, rate in RATES:
                            if interrupt_rate == target:
                                interrupt_rate = rate
                    except KeyError:
                        interrupt_rate =""
                    print("Interrupt Rate: {} - {} - {} => {}".format(region, instance,price["ProductDescription"], interrupt_rate))
                    result.append((regionName, region,price["AvailabilityZone"],price["SpotPrice"], price["InstanceType"],price["ProductDescription"],interrupt_rate))
        return result
    except Exception as e:
        print(e)


#Save spot information data to csv
def save_data_to_csv(result):
    df = DataFrame(result,columns=['regionName','regionCode','AvailabilityZone','SpotPrice','InstanceType','ProductDescription','InterruptRate'])
    df["SpotPrice"] = df["SpotPrice"].apply(pd.to_numeric)
    df.to_csv(RESULT_FILE,index=False)


#This function gives displays which Instance Type is available in an Availability Zone.         
def data_by_availability_and_zone(RESULT_FILE):
    df = pd.read_csv(RESULT_FILE)
    
    '''
    If you want to plot Rows as InstanceType and AvailabilityZone info as column, 
    uncomment the following code below and comment the others.
    
    fig, ax = plt.subplots(figsize=(30, 10))
    df = (df.pivot_table(index=['InstanceType','AvailabilityZone'], aggfunc='size')).unstack(fill_value='-')
    '''
    df = (df.pivot_table(index=['AvailabilityZone','InstanceType'], aggfunc='size')).unstack(fill_value='-') 
    df.replace(to_replace=1,value ='Y', inplace=True)
    visualize_data(df,0)


#This function gives spot price by Availability Zone and Instance Type. 
def current_price_data_by_type_and_zone(RESULT_FILE):
    df = pd.read_csv(RESULT_FILE)
    df=df.pivot(index='AvailabilityZone', columns='InstanceType', values='SpotPrice')
    df=df.fillna("-")
    visualize_data(df,0)
    

#This function gives count of InstanceType that have same AvailabilityZone and Product Description. 
def data_by_description_and_zone(RESULT_FILE):
    df = pd.read_csv(RESULT_FILE)
    df = (df.pivot_table(index=['AvailabilityZone','ProductDescription'], aggfunc='size')).unstack(fill_value=0)
    df.replace(to_replace=0,value ='-', inplace=True)
    visualize_data(df,0)
    

#This function gives count of availability zone that have same InstanceType and Product Description. 
def data_by_description_and_type(RESULT_FILE):
    df = pd.read_csv(RESULT_FILE)
    df = (df.pivot_table(index=['InstanceType','ProductDescription'], aggfunc='size')).unstack(fill_value='-')
    visualize_data(df,0)


#This function gives spot price by Region, Zone and InstanceType. 
def current_price_data_by_instance_region_and_zone(RESULT_FILE):
    df = pd.read_csv(RESULT_FILE)
    df["ZoneType"] = df["AvailabilityZone"]+"-" + df["InstanceType"]
    df=df.pivot(index='ZoneType', columns='regionName', values='SpotPrice')
    df=df.fillna("-")
    visualize_data(df,1)


#This function gives spot price by Region, Zone and ProductDescription. 
def interruptRate_by_instance_region_and_desc(RESULT_FILE):
    df = pd.read_csv(RESULT_FILE)
    df["ZoneRate"] = df["InstanceType"]+" (" + df["ProductDescription"]+")"
    df=df.pivot(index='regionCode', columns='ZoneRate', values='InterruptRate')
    df=df.fillna("-")
    visualize_data(df,1)


#visualize the data
def visualize_data(df,flag):
    
    if flag == 1: 
        fig, ax = plt.subplots(figsize=(15,10))
    else:
        fig, ax = plt.subplots()

    # # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    table_result = ax.table(rowLabels=df.index,
                            cellText=df.values, 
                            colLabels=df.columns,
                            cellLoc = 'center',
                            loc='center')
    table_result.auto_set_font_size(False)
    fig.tight_layout()
    plt.show()
    

def main():
    result = get_spot_information()
    save_data_to_csv(result)
    data_by_availability_and_zone(RESULT_FILE)
    current_price_data_by_type_and_zone(RESULT_FILE)
    data_by_description_and_zone(RESULT_FILE)
    data_by_description_and_type(RESULT_FILE)
    interruptRate_by_instance_region_and_desc(RESULT_FILE)
    
    '''
    This function is resource intensive if there are lots of instances to visualize. 
    By default it is commented out.
    Also the figsize will need to be update to capture the column names.
    '''
    #current_price_data_by_instance_region_and_zone(RESULT_FILE) 
    
    
if __name__ == "__main__":
    main()

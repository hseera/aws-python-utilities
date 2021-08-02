import boto3
import datetime
from botocore.config import Config
import pandas as pd
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt

REGION_CONFIG = Config(
    region_name = 'ap-southeast-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 3
    }
)

RESULT_FILE ="./Data/spotInstance.csv"

def get_spot_price_by_instance():
    
    try:
        client = boto3.client('ec2', config=REGION_CONFIG)
        regions = [x["RegionName"] for x in client.describe_regions()["Regions"]]
        
        
        instances = [x["InstanceType"] for x in client.describe_instance_types()["InstanceTypes"]]
        
        instances =['t3a.small','t3a.xlarge','t3a.2xlarge']
        
        result = []
        
        for instance in instances:
            for region in regions:
                client = boto3.client('ec2',region_name=region)
                Time = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
                prices = client.describe_spot_price_history(
                    InstanceTypes=[instance],
                    ProductDescriptions=['Linux/UNIX','Linux/UNIX (Amazon VPC)','Windows','Windows (Amazon VPC)'],
                    StartTime = Time,
                    MaxResults=1
                    )
                for price in prices['SpotPriceHistory']:
                    available=False
                    #result.append((Time, price["AvailabilityZone"], price["SpotPrice"], price["InstanceType"],price["ProductDescription"]))
                    if pd.to_numeric(price["SpotPrice"]) >=0:
                        available=True
                    result.append((price["AvailabilityZone"], price["SpotPrice"], price["InstanceType"],price["ProductDescription"],available))
        return result
    except Exception as e:
        print(e)


def visualize_data(result):
    df = DataFrame(result,columns=['AvailabilityZone','SpotPrice','InstanceType','ProductDescription','available'])
    df["SpotPrice"] = df["SpotPrice"].apply(pd.to_numeric)
    df.to_csv(RESULT_FILE,index=False)
    print(pd.crosstab(df.AvailabilityZone,df.InstanceType))
    
    # pivot = df.pivot(index='InstanceType', columns='AvailabilityZone', values='SpotPrice')    
    # ax = pivot.T.plot(kind='barh')
    # xlab = ax.set_xlabel('Rate')
    
def main():
    result = get_spot_price_by_instance()
    visualize_data(result)
    
    
    
if __name__ == "__main__":
    main()
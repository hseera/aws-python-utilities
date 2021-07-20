import boto3
from botocore.config import Config
import pandas as pd



#Set region config. It will overwrite region setting done as part of aws access key setup.
REGION_CONFIG = Config(
    region_name = 'ap-southeast-2',
    signature_version = 's3v4',
    retries = {
        'max_attempts': 3
    }
)


def s3_bucket_size(bucket_name):
    s3_client = boto3.client('s3', config=REGION_CONFIG)
    df = pd.DataFrame(columns=['BucketName', 'FileName', 'Size'])
    
    try:
        if bucket_name and not bucket_name.isspace(): #if bucket name is provided
            response = s3_client.list_objects(Bucket=bucket_name)
            df = df[0:0]
            total_size_in_bytes = 0
            if response:
                for key in response['Contents']:
                    df = df.append({'BucketName': bucket_name, 'FileName': key['Key'], 'Size': key['Size']},ignore_index=True)
                    total_size_in_bytes += key['Size']
                print(df)
                print('Bucket name: {}, Size in Bytes:{}\n'.format(bucket_name, total_size_in_bytes))
            
        else:  #when bucket_name is not provided.
            response = s3_client.list_buckets()['Buckets']
            for bucket in response:
                df = df[0:0]
                total_size_in_bytes = 0
                response = s3_client.list_objects(Bucket=bucket['Name'])
                if response:
                    for key in response['Contents']:
                        df = df.append({'BucketName': bucket['Name'], 'FileName': key['Key'], 'Size': key['Size']},ignore_index=True)
                        total_size_in_bytes += key['Size']
                    print(df)
                    print('Bucket name: {}, Size in Bytes:{}\n'.format(bucket['Name'], total_size_in_bytes))
    except Exception as e:
          print(e)


def main():
    bucket_name="my-simple-website"
    s3_bucket_size(bucket_name)
    

    
if __name__ == "__main__":
    main()

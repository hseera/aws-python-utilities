'''
Sample partiQL sql statement template to query DynamoDB  
'''

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


#sample sql example. Replace this with your own PartiQL SQL statment to query dynamoDB.
def sql_statement():
    return {
        "Statement": "SELECT uuid FROM workload"  
    }


def execute_statement():
    dynamodb_client = boto3.client('dynamodb', config=REGION_CONFIG)
    
    try:
        input = sql_statement()
        response = dynamodb_client.execute_statement(**input)
        '''
        Add your own action to perform on the result set.
        '''
        print(response['uuid'])
        print("Statement executed successfully.")

    except Exception as error:
        print(error)



def main():
    #Execute SQL statement
    execute_statement()
  

if __name__ == "__main__":
    main()
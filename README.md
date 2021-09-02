# aws-python-utilities
![Language Python](https://img.shields.io/badge/%20Language-python-blue.svg) [![Apache License](http://img.shields.io/badge/License-Apache-blue.png)](LICENSE)

[![GitHub Last Commits](https://img.shields.io/github/last-commit/hseera/aws-python-utilities.svg)](https://github.com/hseera/aws-python-utilities/commits/) [![GitHub Size](https://img.shields.io/github/repo-size/hseera/aws-python-utilities.svg)](https://github.com/hseera/aws-python-utilities/)
[![Open GitHub Issue](https://img.shields.io/badge/Open-Incident-brightgreen.svg)](https://github.com/hseera/aws-python-utilities/issues/new/choose)
[![GitHub Open Issues](https://img.shields.io/github/issues/hseera/aws-python-utilities?color=purple)](https://github.com/hseera/aws-python-utilities/issues?q=is%3Aopen+is%3Aissue)
[![GitHub Closed Issues](https://img.shields.io/github/issues-closed/hseera/aws-python-utilities?color=purple)](https://github.com/hseera/aws-python-utilities/issues?q=is%3Aclosed+is%3Aissue)

Python utilities for AWS. These utilities help save time with different facets (RCA/reporting/cost saving) of performance testing as part of devops or standalone.
The readme page will continue to get updated as and when, I add new utility to the repo.

---
|Utility Link |Utility Link|
|:-----|:------|
|[1: Cloudwatch Metrics To Image](#1-cloudwatch-metrics-to-image)|[2: Update DynamoDB Insights](#2-update-dynamodb-insights)|
|[3: Update Dynamodb Capacity](#3-update-dynamodb-capacity)|[4: Cloudwatch Dashboards](#4-cloudwatch-dashboards)|
|[5: Compare Query And Scan](#5-compare-query-and-scan)|[6: Compare Get And Batch Get Item](#6-compare-get-and-batch-get-item)|
|[7: Bucket Size](#7-bucket-size)|[8: Copy DynamoDB Table](#8-copy-dynamodb-table)|
|[9: Sample PartiQL DynamoDB Script](#9-sample-partiql-dynamodb-script)|[10: Spot Instance info](#10-spot-instance-info)|
|[11: Stop Start EC2](#11-stop-start-ec2)|[12: Synthetic Monitoring](#12-synthetic-monitoring)|
|[13: SQS Playa](#13-sqs-playa)||

# [1: Cloudwatch Metrics To Image](#1-cloudwatch-metrics-to-image)
![index](https://github.com/hseera/aws-python-utilities/blob/main/images/cloudwatch-metrics.png)

This simple utility allows you to generate Images for the Cloudwatch Metrics. There are times when you want to have an Image for reporting purposes (for example, Performance TSR). This utility reduces the effort required to generate the Image manually. It saves a lot of time when you have lots of Images to generate. 

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to execute the script

```
1: awscli
2: boto3
3: python 3.5
4: Setup your AWS Access, Secret key and the AWS region

```

### Execution

```
1: Make sure above prerequisite are met first.
2: Update the FileName in the script to where you want to save the Image.
3: Update the timezone setting in the script.
4: If AWS access setup has a different AWS region then you can overwrite it in the RegionConfig parameter in the script. Otherwise comment it out.
5: Replace the default json payload with the correct Image API json playload. Correct json payload can be copied from the Cloudwatch console. 
6: Now execute the python script by passing in the start and end time in epoch (ms) for which you want to generate the Image.

```


# [2: Update DynamoDB Insights](#2-update-dynamodb-insights)
![index](https://github.com/hseera/aws-python-utilities/blob/main/images/dynamodb-insights.png)

This simple utility allows you to enable or disable dynamodb contributor insights. Pass the table name in the script for which you want contributor insights enabled or disabled.  Contributor Insights helps you identify which dynamodb partition is highly accessed. It is useful for DynamoDB table RCA.

### Prerequisites

What things you need to execute the script

```
1: awscli
2: boto3
3: python 3.5
4: Setup your AWS Access, Secret key and the AWS region

```

### Execution

```
1: Make sure above prerequisite are first met.
2: Replace the default value for the variable "TABLE_TO_UPDATE" with your table name.
3: If AWS access setup has a different AWS region then you can overwrite it in the RegionConfig parameter in the script. Otherwise comment it out.
4: Now execute the python script.

```


# [3: Update Dynamodb Capacity](#3-update-dynamodb-capacity)
There might be cases when you end up having a lot of DynamoDB tables in your  non-prod environment and they might be either set to Provisioned or On-Demand capacity. If they are not properly managed, cost ($$) of keeping these tables on Provisioned capacity can escalate pretty quickly. This simple python script goes through all the tables and if they are on provisioned capacity changes them to On-demand. If they are already on On-Demand capacity, it doesn't nothing. 

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to execute the script

```
1: awscli
2: boto3
3: python 3.5
4: Setup your AWS Access, Secret key and the AWS region

```

### Execution

```
Once above prequisites are setup, execute the python script
```

### Improvements

* Check when was the table last changed to On-Demand capacity. If it was less than 24 hours than reduce the Provisioned capacity else change it to On-Demand.
* Improve on the get() function call. In future if AWS changes the json structure, this call if fail. Need to come up with a better approach. 


# [4: Cloudwatch Dashboards](#4-cloudwatch-dashboards)
![index](https://github.com/hseera/aws-python-utilities/blob/main/images/cloudwatch-dashboards.png)
This simple utility allows you to create or delete cloudwatch dashboards. Useful when you need to create multiple dashboards.

### Prerequisites

What things you need to execute the script

```
1: awscli
2: boto3
3: python 3.5
4: Setup your AWS Access, Secret key and the AWS region

```

### Execution

```
1: Make sure above prerequisite are first met.
2: Replace the default payload for the variable "DASHBOARD_JSON" with your dashboard json payload. Best way is to take an exisiting dashboard payload from console, modify it and pass it into the script (if you are creating a dashboard).
3: Replace the default value for the variable "DASHBOARD_NAME" with your dashboard name.
4: If AWS access setup has a different AWS region then you can overwrite it in the RegionConfig parameter in the script. Otherwise comment it out.
5: Now execute the python script.

```


# [5: Compare Query And Scan](#5-compare-query-and-scan)
![index](https://github.com/hseera/aws-python-utilities/blob/main/images/query_scan.png)

Compare DynamoDB Query vs Scan time.

# [6: Compare Get And Batch Get Item](#6-compare-get-and-batch-get-item)
![index](https://github.com/hseera/aws-python-utilities/blob/main/images/get-batchitem.png)

Compare DynamoDB GetItem and BatchGetItem API calls.

# [7: Bucket Size](#7-bucket-size)
![index](https://github.com/hseera/aws-python-utilities/blob/main/images/bucket-size.png)

Get S3 Bucket Size.

# [8: Copy DynamoDB Table](#8-copy-dynamodb-table)
This script takes a backup of a dynamodb table and copy's the data to a different dynamodb table. 
During the process, the data is first saved to S3 bucket.

# [9: Sample PartiQL DynamoDB Script](#9-sample-partiql-dynamodb-script)
A sample python script example to execute SQL statement against DynamoDB.

# [10: Spot Instance info](#10-spot-instance-info)
Script to help extract spot instance information to answer questions such as:
1. What is the current spot instance price in each region?
2. What type of spot instances are available in a region & availability zone?
3. What is the interruption rate for a spot instance?
4. What OS is available for a spot instance in a region & availability zone?

![index](https://github.com/hseera/aws-python-utilities/blob/main/images/location-price.png)

![index1](https://github.com/hseera/aws-python-utilities/blob/main/images/interrupt_rate.png)



# [11: Stop Start EC2](#11-stop-start-ec2)
Script gives the capability to stop & start ec2 instanced based on instanceid, instance type or platform.

## Stop & Start All Instances

```
./stop_start_ec2.py stop id
./stop_start_ec2.py start id
```

## Stop & Start By Instance type

```
./stop_start_ec2.py stop type <<instance type>>
./stop_start_ec2.py start type <<instance type>>
```
example
```
./stop_start_ec2.py stop type t2.micro
./stop_start_ec2.py start type t2.micro
```

## Stop & Start By Platform
Pass "windows" if you want to stop or start Windows platform. Otherwise pass other.

```
./stop_start_ec2.py stop platform windows
./stop_start_ec2.py start platform windows
```
or
```
./stop_start_ec2.py stop platform other
./stop_start_ec2.py start platform other
```

## Stop & Start By Platform And InstanceType
Pass "windows" if you want to stop or start Windows platform. Otherwise pass other.
Also pass in what Instance type you want to stop or start.

```
./stop_start_ec2.py stop windows {InstanceType}
./stop_start_ec2.py start windows {InstanceType}
```
or
```
./stop_start_ec2.py stop other {InstanceType}
./stop_start_ec2.py start other {InstanceType}
```

example
```
./stop_start_ec2.py stop windows t2.micro
./stop_start_ec2.py start other t2.micro
./stop_start_ec2.py start windows t2.small
./stop_start_ec2.py stop other c4.2xlarge
```

## Requirements
### Python Modules
If you never used Amazon Web Services with Python before, you have to install two additional modules:
```
pip install boto3 botocore
```
or
```
pip3 install boto3 botocore
```
### AWS Credentials
Save your AWS Credentials in your home/users folder:

Linux:
```
/home/[username]/.aws
```

Windows:
```
/Users/[username]/.aws
```
For more information about the content of the .aws folder check the AWS documentation: [Configuration and Credential Files.](https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html)

Instead of creating the .aws folder manually you can use the [AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html):

* [Installer for Windows](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-windows.html#install-msi-on-windows)
* [Installer for Linux, UNIX](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-bundle.html)

After you've installed the AWS CLI open the PowerShell (or the Command Prompt) in Windows. In UNIX-like systems open a Shell. Then run the following command:
```
aws configure
```
Enter

* your AWS Access Key ID and
* your AWS Secret Access Key.
* As default region name enter your Availability Zone (AZ) and
* use "json" as default output format

# [12: Synthetic Monitoring](#12-synthetic-monitoring)
Script gives you the capability to Start,Stop, Delete & Create canaries. You can also query to get script runtime version, which is required to create a canary.

## Star & Stop All canaries

```
./synthetic_canary.py stop
./synthetic_canary.py start
```

## Star & Stop a canary

```
./synthetic_canary.py stop/start <<canary name>>
```
example
```
./synthetic_canary.py stop workload
./synthetic_canary.py start workload
```

## Delete a canary

```
./synthetic_canary.py delete {canary name}
```
example
```
./synthetic_canary.py delete workload
```

## Script Runtime Version
Returns a list of Synthetics canary runtime versions and their dependencies.
```
./synthetic_canary.py runtime
```


## Create a canary

```
./synthetic_canary.py create {canary name}
```
example
```
./synthetic_canary.py create workload
```

## Requirements
### Python Modules
If you never used Amazon Web Services with Python before, you have to install two additional modules:
```
pip install boto3 botocore
```
or
```
pip3 install boto3 botocore
```
### AWS Credentials
Save your AWS Credentials in your home/users folder:

Linux:
```
/home/[username]/.aws
```

Windows:
```
/Users/[username]/.aws
```
For more information about the content of the .aws folder check the AWS documentation: [Configuration and Credential Files.](https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html)

Instead of creating the .aws folder manually you can use the [AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html):

* [Installer for Windows](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-windows.html#install-msi-on-windows)
* [Installer for Linux, UNIX](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-bundle.html)

After you've installed the AWS CLI open the PowerShell (or the Command Prompt) in Windows. In UNIX-like systems open a Shell. Then run the following command:
```
aws configure
```
Enter

* your AWS Access Key ID and
* your AWS Secret Access Key.
* As default region name enter your Availability Zone (AZ) and
* use "json" as default output format


# [13: SQS Playa](#13-sqs-playa)
GUI utility for Windows OS to send message to AWS SQS.
Currently MVP status. More feature and improvements will be added to it.

Current version requires you to build exe from the code.
![index](https://github.com/hseera/aws-python-utilities/blob/main/images/sqs-playa.png)


## Requirements
### Python Modules
If you never used Amazon Web Services with Python before, you have to install the following modules:
```
boto3 
botocore
PySimpleGUI
import boto3
icecream

```

### AWS Credentials
Save your AWS Credentials in your home/users folder:

Linux:
```
/home/[username]/.aws
```

Windows:
```
/Users/[username]/.aws
```
For more information about the content of the .aws folder check the AWS documentation: [Configuration and Credential Files.](https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html)

Instead of creating the .aws folder manually you can use the [AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html):

* [Installer for Windows](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-windows.html#install-msi-on-windows)
* [Installer for Linux, UNIX](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-bundle.html)

After you've installed the AWS CLI open the PowerShell (or the Command Prompt) in Windows. In UNIX-like systems open a Shell. Then run the following command:
```
aws configure
```
Enter

* your AWS Access Key ID and
* your AWS Secret Access Key.
* As default region name enter your Availability Zone (AZ) and
* use "json" as default output format

# Contribute

If you would like to contribute to this project, please reachout to me. Issues and pull requests are welcomed too.

# Author
[<img id="github" src="./images/github.png" width="50" a="https://github.com/hseera/">](https://github.com/hseera/)    [<img src="./images/linkedin.png" style="max-width:100%;" >](https://www.linkedin.com/in/hpseera) [<img id="twitter" src="./images/twitter.png" width="50" a="twitter.com/HarinderSeera/">](https://twitter.com/@HarinderSeera) <a href="https://twitter.com/intent/follow?screen_name=harinderseera"> <img src="https://img.shields.io/twitter/follow/harinderseera.svg?label=Follow%20@harinderseera" alt="Follow @harinderseera" /> </a>          [![GitHub followers](https://img.shields.io/github/followers/hseera.svg?style=social&label=Follow&maxAge=2592000)](https://github.com/hseera?tab=followers)


# License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details

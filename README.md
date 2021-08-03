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

![index](https://github.com/hseera/aws-python-utilities/blob/main/images/interrupt-rate.png)


## Contribute

If you would like to contribute to this project, please reachout to me. Issues and pull requests are welcomed too.

## Author
[<img id="github" src="./images/github.png" width="50" a="https://github.com/hseera/">](https://github.com/hseera/)    [<img src="./images/linkedin.png" style="max-width:100%;" >](https://www.linkedin.com/in/hpseera) [<img id="twitter" src="./images/twitter.png" width="50" a="twitter.com/HarinderSeera/">](https://twitter.com/@HarinderSeera) <a href="https://twitter.com/intent/follow?screen_name=harinderseera"> <img src="https://img.shields.io/twitter/follow/harinderseera.svg?label=Follow%20@harinderseera" alt="Follow @harinderseera" /> </a>          [![GitHub followers](https://img.shields.io/github/followers/hseera.svg?style=social&label=Follow&maxAge=2592000)](https://github.com/hseera?tab=followers)


## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details
# aws-python-utilities
Python utilities for AWS. 


## Cloudwatch Metrics Image Generation Utility
![index](https://github.com/hseera/aws-python-utilities/blob/main/images/cloudwatch-metrics.png)

This simple utility allows you generate Images for the Cloudwatch Metrics. There are times when you want to have an Image for reporting purposes (for example, Performance TSR). This utility reduces the effort required to generate the Image manually. It saves a lot of time when you have lots of Images to generate. 

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



## update-dynamodb-insights
![index](https://github.com/hseera/aws-python-utilities/blob/main/images/dynamodb-insights.png)

This simple utility allows you to enable or disable dynamodb contributor insights. Pass the table name in the script for which you want contributer insights enabled or disabled.

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

## Update dynamodb capacity
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

## Authors

* **Harinder Seera** - *Initial work* - [OzPerf](https://ozperf.com/)

If you would like to contribute to this project, please reachout to me.

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details
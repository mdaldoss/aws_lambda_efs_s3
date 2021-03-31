# aws_lambda_efs_s3 - UPDATED MARCH 2021
An example project that shows how to extend AWS lambda with EFS (Elastic File Storage) and load package layers from S3 space

## Motivation
This come from my struggle to make work an lambda function where I need extra space in order to load libraries and larger code
It can be used as well to download your latest machine learning model from an S3 storage space.
Lambda function are indeed (as today) limited to 512 MB /tmp space.

## Solution
The solution adopted has been by extend it by attaching an extra volume EFS. 
Someone might encounter that this activity actually might block S3 connection p


## STEPS
1) Add AWS EFS (Elastic File Storage) to your lambda
2) Add endpoint to your VPC to access S3 storage
3) Add EFS mount point in lambda
4) Upload your code

### 1) Create EFS 
In AWS console search EFS.
Select create.
After creating your EFS:
-> press "Access point" and create one with the following:
"Root directory path" = "/mnt/your-efs-name" _IMPORTANT!_ -> This will be your mount point on your aws lambda too!
"User ID" = 1000
"Group ID" = 1000
"Root directory creation permissions"
"Owner user ID" = 1000
"Owner group ID" = 1000
"Permissions" = 777 -> or what you prefer

### 2) Set Enpoint to S3 Storage
In AWS console, go to *VPC*
- then select at the menu on the left *endopoint*
- &nbsp Create Endpoint
- &nbsp&nbsp Service Category: AWS Services
- &nbsp&nbsp In "Service name" search for: "S3 GATEWAY"
- &nbsp&nbsp Choose "Full acccess"
- &nbsp&nbsp In "Configure route tables" select your subnets
- &nbsp&nbsp Press "Create Endpoint"
  
 (reference https://aws.amazon.com/blogs/aws/new-vpc-endpoint-for-amazon-s3/)
 
### 3) EFS mount point
In your lambda select
- Configuration
  -> File system
    -> Select your Access point
    -> Set your "Local mount path" the same as the one you set in the EFS Access point!
    
### 4) CODE
Enjoy!



-> Marco Daldoss - March 2021 <- 

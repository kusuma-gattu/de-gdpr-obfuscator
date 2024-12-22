# Data GDPR Obfuscation Tool
### Project Description
This project provides a general-purpose Python tool to obfuscate Personally Identifiable Information (PII) in data files stored in AWS S3. The tool intercepts PII in files, such as CSV files, and replaces sensitive fields with obfuscated strings. This project is intended to ensure data privacy and compliance with GDPR standards by anonymizing specified fields before processing or sharing data further.

The goal of this project is to develop a library module that can be integrated into a Python codebase. Given the S3 location of a file and the field names of PII data, this tool generates an obfuscated version of the file as a byte-stream object. The calling application is responsible for saving the output data to a desired destination.


### Prerequisites and Assumptions
AWS CLI Configure Profile: configure your IAM role on AWS CLI using command aws configure

GitHub Secret Keys: configure GitHub Secrets for AWS IAM access key, secret access key and region

S3 Bucket: replace S3 bucket name with your bucket in vars.tf file under terraform, and make sure you have files in specified bucket. This accepts CSV, JSON and Parquet file formats

### High-Level Workflow
Input: The tool is triggered by sending a JSON string specifying:
The S3 location of the data file.
A list of fields that require obfuscation.

Processing: The tool retrieves the data file, obfuscates the specified PII fields, and produces an exact copy of the original file with PII fields replaced by obfuscated strings.

Output: A byte-stream representation of the obfuscated file that can be directly used with the boto3 S3 Put Object function for saving the file back to AWS S3 or elsewhere.

### Run the Project
Code will be deployed using GitHub Actions pipeline.

There are 2 ways to run this project

#### Option 1:
Step 1. Grab the ARN of step function from AWS console

step 2. start execution of step function using the follow command on AWS CLI

aws stepfunctions start-execution \
--state-machine-arn "paste step function arn here" \
--input '{
"file_to_obfuscate": "paste S3 Object URI here",
"pii_fields": ["list", "all", "pii", "columns", "here"] 
}'

example : 

aws stepfunctions start-execution \
    --state-machine-arn "arn:aws:states:<region>:<account-id>:stateMachine:InvokeLambdaAndRetrieveFile" \
    --input '{
            "file_to_obfuscate": "s3://bucket_name/sample.csv",
            "pii_fields": ["name", "email"]
        }'


#### Option 2:
step 1: go to 'terraform' folder of the project/repo in AWS CLI
step 2: start execution of step function using the follow command 

aws stepfunctions start-execution \
--state-machine-arn "$(terraform output -raws state_machine_arn)" \
--input '{
"file_to_obfuscate": "paste S3 Object URI here",
"pii_fields": ["list", "all", "pii", "columns", "here"] 
}'

example:

aws stepfunctions start-execution \
--state-machine-arn "$(terraform output -raws state_machine_arn)" \
--input '{
            "file_to_obfuscate": "s3://bucket_name/sample.csv",
            "pii_fields": ["email", "contact"]
        }'




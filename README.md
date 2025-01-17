# Data GDPR Obfuscation Tool

## Project Description
The **Data GDPR Obfuscation Tool** is a Python-based solution designed to anonymize Personally Identifiable Information (PII) in data files stored in AWS S3. By obfuscating sensitive fields, such as names and email addresses, the tool ensures data privacy and compliance with GDPR standards. This solution is particularly useful for organizations aiming to protect sensitive data during processing or sharing.

This project provides a library module that can be seamlessly integrated into Python applications. Given the S3 location of a data file and the field names containing PII, the tool generates an obfuscated version of the file as a byte-stream object. The calling application is responsible for saving the processed file to a desired location.

---

## Prerequisites and Assumptions

### AWS Configuration
- Configure your IAM role on the AWS CLI using the following command:
  ```bash
  aws configure
  ```

### GitHub Secrets
- Configure GitHub Secrets to store the following:
  - AWS IAM Access Key
  - AWS IAM Secret Access Key
  - AWS Region

### S3 Bucket
- This project expects two S3 buckets exist in AWS:
  1. To store terraform state files:
     - If you have already have a bucket then replace the `bucket` argument in `main.tf` file under the Terraform configuration.
     - Otherwise, Create a S3 bucket with a globally unique name in AWS console and replace the `bucket` argument with the recently created bucket name in `main.tf` file under the Terraform configuration.
  2. S3 bucket which contains data files. 
     - Update with your S3 bucket name in the `vars.tf` file under the Terraform configuration. Ensures that this bucket has data files

### Supported File Formats
- The tool supports the following file formats:
  - CSV
  - JSON
  - Parquet

---

## High-Level Workflow

### Input
1. Specify the S3 location of the data file.
2. Provide a list of fields that require obfuscation.
   ```bash
   input might look like this:
   {
    "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file_01.csv", 
    "pii_fields": ["name", "email"]
   }

   The target CSV file might look like this:
   
   student_id,name,course,cohort,graduation_date,email_address
   ...
   1234,'John Smith','Software','2024-03-31','j.smith@email.com' 
   ...
   ```

### Processing
1. The tool retrieves the specified data file from S3.
2. Obfuscates the specified PII fields by replacing them with anonymized values.
3. Produces an exact copy of the original file with the PII fields obfuscated.

### Output
- A byte-stream representation of the obfuscated file would be found in aws state functions output

  ```bash
  The output will be a byte-stream representation of a file look like this:
  
  student_id,name,course,cohort,graduation_date,email_address
  ...
  1234,'****','Software','2024-03-31','****'
  ...
  ```


---

## Running the Project
The project is deployed in two ways.

1. Through CI/CD pipeline
2. Run code locally

### **Option 1: Using CI/CD pipeline**

1. The project will be deployed automatimatically by GitHub actions workflow, once the codebase is pushed or pull request made on main branch of Github
2. Retrieve the ARN of the Step Function from the AWS Management Console, once the repo is deployed on AWS.
3. Start the Step Function execution using the following command on AWS CLI of Linux or Mac OS machine:
   ```bash
   aws stepfunctions start-execution \
     --state-machine-arn "<STEP_FUNCTION_ARN>" \
     --input '{ "file_to_obfuscate": "<S3_OBJECT_URI>", "pii_fields": ["<PII_FIELD_1>", "<PII_FIELD_2>"] }'
   ```
  
#### Example
```bash
aws stepfunctions start-execution \
  --state-machine-arn "arn:aws:states:us-east-1:123456789012:stateMachine:InvokeLambdaAndRetrieveFile" \
  --input '{ "file_to_obfuscate": "s3://my-bucket/sample.csv", "pii_fields": ["name", "email"] }'
```
Start the Step Function execution using the following command on AWS CLI of Windows OS machine:
```bash
aws stepfunctions start-execution \
--state-machine-arn "<STEP_FUNCTION_ARN>" \
--input "{\"file_to_obfuscate\": \"<S3_OBJECT_URI>\", \"pii_fields\": [\"<PII_FIELD_1>\", \"<PII_FIELD_2>\"]}"
```

### **Option 2: Run the code locally**


#### Project Build and Testing Instructions
This project uses a Makefile to automate the setup, testing and code quality checks. Below are the instructions for building and running various checks on the project locally.

##### Prerequisites

Ensure you have the following installed on your machine:
- Python 3.x
- `make` command utility

1. Create virtual environment and install the necessary dependencies for the project
```bash
make install-dependencies
```

2. To perform security checks on the project, use:
```bash
make run-security
```

3. To run unit tests and test coverage, execute:
```bash
make run-tests
```

4. To execute all necessary setup, security checks and unit tests all at once, use:
```bash
make run-all
```

5. Navigate to the `terraform` folder of the repository.

6. Run the following commands to deploy locally:
    - initialize the terraform:
      ```bash
      terraform init
      ```
    - plan the configuration:
      ```bash
      terraform plan
      ```
    - deploy the resources:
      ```bash
      terrafrom apply
      ```
      enter `yes` when prompted

7. Start the Step Function execution using the following command on Linux or Mac OS once resources are deployed:

   ```bash
   aws stepfunctions start-execution \
     --state-machine-arn "$(terraform output -raw state_machine_arn)" \
     --input '{ "file_to_obfuscate": "<S3_OBJECT_URI>", "pii_fields": ["<PII_FIELD_1>", "<PII_FIELD_2>"] }'
   ```

#### Example
```bash
aws stepfunctions start-execution \
  --state-machine-arn "$(terraform output -raw state_machine_arn)" \
  --input '{ "file_to_obfuscate": "s3://my-bucket/sample.csv", "pii_fields": ["email", "address"] }'
```

Start the Step Function execution using the following command on Windows OS:
```bash
aws stepfunctions start-execution \
--state-machine-arn "$(terraform output -raw state_machine_arn)" \
--input "{\"file_to_obfuscate\": \"<S3_OBJECT_URI>\", \"pii_fields\": [\"<PII_FIELD_1>\", \"<PII_FIELD_2>\"]}"
```

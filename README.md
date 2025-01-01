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
- create a S3 bucket with name: "de-gdpr-obfuscator-terraform-statefiles" to store terraform state filesgit
- Update the S3 bucket name in the `vars.tf` file under the Terraform configuration.
- Ensure that the data files are present in this bucket.

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

### Processing
1. The tool retrieves the specified data file from S3.
2. Obfuscates the specified PII fields by replacing them with anonymized values.
3. Produces an exact copy of the original file with the PII fields obfuscated.

### Output
- A byte-stream representation of the obfuscated file would be found in aws state functions output

---

## Running the Project
The project is deployed using a GitHub Actions pipeline and can be executed in two ways.

### **Option 1: Using the AWS CLI**

1. Retrieve the ARN of the Step Function from the AWS Management Console.
2. Start the Step Function execution using the following command on Linux or Mac OS:
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
Start the Step Function execution using the following command on Windows OS:
```bash
aws stepfunctions start-execution \
--state-machine-arn "<STEP_FUNCTION_ARN>" \
--input "{\"file_to_obfuscate\": \"<S3_OBJECT_URI>\", \"pii_fields\": [\"<PII_FIELD_1>\", \"<PII_FIELD_2>\"]}"
```

### **Option 2: Using Terraform**

1. Navigate to the `terraform` folder of the repository.
2. Start the Step Function execution using the following command on Linux or Mac OS:
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

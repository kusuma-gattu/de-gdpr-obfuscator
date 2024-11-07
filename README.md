# Data Obfuscation Tool
### Overview
This project provides a general-purpose Python tool to obfuscate Personally Identifiable Information (PII) in data files stored in AWS S3. The tool intercepts PII in files, such as CSV files, and replaces sensitive fields with obfuscated strings. This project is intended to ensure data privacy and compliance with GDPR standards by anonymizing specified fields before processing or sharing data further.

### Prerequisites and Assumptions
Data Format: Input data is stored in CSV, JSON, or Parquet formats in an AWS S3 bucket.

PII Fields: Fields containing GDPR-sensitive data are known and provided in advance.

### Project Goal
The goal of this project is to develop a library module that can be integrated into a Python codebase. Given the S3 location of a file and the field names of PII data, this tool generates an obfuscated version of the file as a byte-stream object. The calling application is responsible for saving the output data to a desired destination.

### High-Level Workflow
Input: The tool is triggered by sending a JSON string specifying:
The S3 location of the data file.
A list of fields that require obfuscation.

Processing: The tool retrieves the data file, obfuscates the specified PII fields, and produces an exact copy of the original file with PII fields replaced by obfuscated strings.

Output: A byte-stream representation of the obfuscated file that can be directly used with the boto3 S3 Put Object function for saving the file back to AWS S3 or elsewhere.

# Define variables which used across the Terraform configurations

variable "lambda_name" {
    type = string
    default = "obfuscator_tool"
}

variable "s3_bucket_name" {
    type = string
    # REPLACE HERE with YOUR S3 BUCKET NAME
    default = "gdpr-ingestion-zone"
}

variable "step_function_name" {
    type = string
    default = "InvokeLambdaAndRetrieveFile"
}

# variable "terraform-statefile" {
#     type = string
#     default = "de-gdpr-obfuscator-terraform-statefiles"
# }

# create and configure lambda function and it's dependencies
resource "aws_lambda_function" "obfuscator_tool" {
    function_name = "${var.lambda_name}"
    role = aws_iam_role.lambda_role.arn
    filename = data.archive_file.obfuscator_tool_zip.output_path
    source_code_hash = data.archive_file.obfuscator_tool_zip.output_base64sha256
    layers = ["arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python312:14"]
    handler = "obfuscator_tool.lambda_handler"
    runtime = "python3.12"
    # performance criteria
    timeout = 60
}


data "archive_file" "obfuscator_tool_zip" {
    type = "zip"
    source_file = "${path.module}/../src/obfuscator_tool.py"
    output_path = "${path.module}/../src/obfuscator_tool.zip"
}

# Define IAM roles and attach necessary policies to Lambda, S3 

# policy document for lambda
data "aws_iam_policy_document" "assume_role" {
    statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}


# define the lambda role
resource "aws_iam_role" "lambda_role" {
    name_prefix = "role-${var.lambda_name}-" 
    assume_role_policy = data.aws_iam_policy_document.assume_role.json
    
}

# attach S3 role to lambda role
resource "aws_iam_role_policy_attachment" "lambda_s3_role_attachment" {
    role = aws_iam_role.lambda_role.name
    policy_arn = aws_iam_policy.s3_policy.arn
}

# attach cloud watch logs to lambda
resource "aws_iam_role_policy_attachment" "lambda_cw_role_attachment" {
    role = aws_iam_role.lambda_role.name
    policy_arn = aws_iam_policy.cw_log_policy.arn
}
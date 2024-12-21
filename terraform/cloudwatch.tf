# Define IAM policies and Cloudwatch log groups/streams to manage and monitor logs fro Lambda

# Get the current account identity and region
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# IAM policy for Cloudwatch log permissions for lambda function
resource "aws_iam_policy" "cw_log_policy" {
    name = "CloudWatchLogPermissions"
    description = "IAM policy for Lambda CloudWatch log permissions"
    policy = jsonencode({
         Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams",
          "logs:GetLogEvents",
          "logs:FilterLogEvents"
        ]
        Resource = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.lambda_name}:*"
        
      }
    ]
    })
}
# Define IAM role and attach necessary policies to step function to invoke lambda

data "aws_iam_policy_document" "step_function_policy_doc" {
    statement {
        effect = "Allow"
        principals {
          type = "Service"
          identifiers = ["states.amazonaws.com"]
        }
        actions = ["sts:AssumeRole"]
    }
 
}

resource "aws_iam_role" "step_function_role" {
    name = "step-function-role"
    assume_role_policy = data.aws_iam_policy_document.step_function_policy_doc.json   
}

resource "aws_iam_role_policy" "sf_lambda_policy" {
  name = "step-function-lambda-policy"
  role = "${aws_iam_role.step_function_role.id}"
  policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
          {
            Effect   = "Allow"
            Action   = ["lambda:InvokeFunction"]
            Resource = "${aws_lambda_function.obfuscator_tool.arn}"
          }
        ]
      })
}

resource "aws_sfn_state_machine" "step_function" {
  name     = var.step_function_name
  role_arn = "${aws_iam_role.step_function_role.arn}"

  definition = jsonencode({
    Comment: "Step Function to invoke Lambda and retrieve a file",
    StartAt: "Invoke Lambda",
    States: {
      "Invoke Lambda": {
        Type: "Task",
        Resource: "${aws_lambda_function.obfuscator_tool.arn}",
        InputPath: "$",
        ResultPath: "$.lambda_result",
        Next: "Process File"
      },
      "Process File": {
        Type: "Pass",
        Parameters: {
          "file.$": "$.lambda_result.file"
        },
        End: true
      }
    }
  })
}

output "state_machine_arn" {
  description = "ARN of the Step Function"
  value       = "${aws_sfn_state_machine.step_function.arn}"
}




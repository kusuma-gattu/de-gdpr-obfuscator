# create S3 bucket for terraform state files
resource "aws_s3_bucket" "terraform_statefile" {
    bucket_prefix = "${var.terraform-statefile}-"

    tags = {
        Name = "de-gdpr-obfuscator-terraform-statefiles"
        Environment = "Dev"
    }
}

# access existing s3 bucket
data "aws_s3_bucket" "s3_ingestion_zone" {
    bucket = "${var.s3_bucket_name}"
} 


# S3 policy document
data "aws_iam_policy_document" "s3_policy_doc" {
    statement {
    actions = [
      "s3:GetObject",
      "s3:ListBuckets",
      "s3:PutObject",
      "s3:ListObjectsV2",
      "s3-object-lambda:*",
    ]

    resources =  [
        "${data.aws_s3_bucket.s3_ingestion_zone.arn}/*"
    ]
  }
}

# define s3 policy
resource "aws_iam_policy" "s3_policy" {
    name = "s3_policy"
    policy = data.aws_iam_policy_document.s3_policy_doc.json
}

provider "aws" {
    region = "eu-west-2"

    default_tags {
        tags = {
            Project = "GDPR Obfuscator Tool"
            Team = "Freelance"
            Environment = "Dev"
            Timeline = "31-12-2024" 
        }
    }
}

terraform {
    backend "s3" {
      region = "eu-west-2"
      bucket= "${aws_s3_bucket.terraform_statefile.bucket}"
      key = "extract-statefile"
    }
}

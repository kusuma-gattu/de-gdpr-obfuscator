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
      # REPLACE HERE with YOUR S3 BUCKET NAME, which you have created to store terraform state files.   
      bucket= "de-gdpr-obfuscator-terraform-statefiles"
      key = "extract-statefile"
    }
}

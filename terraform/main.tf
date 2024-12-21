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
variable "region" {
  description = "AWS region"
  default     = "eu-west-1"
}

variable "github_actions_ip" {
  description = "GitHub Actions IP range"
  type        = string
  # This should be set via terraform.tfvars or environment variables
}
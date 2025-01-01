provider "aws" {
  region = var.region
}

# Crear el bucket de S3 para el estado de Terraform
resource "aws_s3_bucket" "terraform_state" {
  bucket = "mi-bucket-terraform-state"  # Cambia esto por un nombre único

  tags = {
    Name        = "TerraformState"
    Description = "Bucket para almacenar el estado de Terraform"
  }
}

# Crear la tabla DynamoDB para bloqueo de Terraform
resource "aws_dynamodb_table" "terraform_locks" {
  name           = "tabla-de-lock-terraform"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
  tags = {
    Name        = "Terraform Lock Table"
    Description = "Table for managing Terraform state locks"
  }
}
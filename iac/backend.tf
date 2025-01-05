# Configuración del backend para almacenar el estado de Terraform
terraform {
  backend "s3" {
    bucket         = "mi-bucket-terraform-state"  # Cambia esto por un nombre único
    key            = "terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "tabla-de-lock-terraform"
  }
}

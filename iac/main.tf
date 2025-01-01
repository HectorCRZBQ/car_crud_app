provider "aws" {
  region = var.region
}

# Crear el bucket de S3 para el estado de Terraform con un nombre único
resource "aws_s3_bucket" "terraform_state" {
  bucket = local.bucket_name

  tags = {
    Name        = "TerraformState"
    Description = "Bucket para almacenar el estado de Terraform"
  }
}

# Nombre único para el bucket S3 basado en un prefijo y un sufijo generado
locals {
  bucket_name = "mi-bucket-terraform-state-${random_string.suffix.result}"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
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

# Backend de Terraform (con S3 y DynamoDB para bloqueos)
terraform {
  backend "s3" {
    bucket         = local.bucket_name
    key            = "terraform.tfstate"
    region         = var.region
    encrypt        = true
    dynamodb_table = aws_dynamodb_table.terraform_locks.name
  }
}

# Crear VPC principal
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name        = "Main-VPC"
    Description = "VPC principal para la infraestructura"
  }
}

# Crear subred pública dentro de la VPC
resource "aws_subnet" "main" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[0]
  tags = {
    Name        = "Main-Subnet"
    Description = "Subred pública asociada a la VPC principal"
  }
}

# Crear una puerta de enlace de Internet para la VPC
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name        = "Main-IGW"
    Description = "Puerta de enlace de Internet para la VPC"
  }
}

# Crear una tabla de rutas para la subred pública
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name        = "Main-RouteTable"
    Description = "Tabla de rutas para la VPC"
  }
}

# Asociar la tabla de rutas a la subred pública
resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}

# Crear un grupo de seguridad que permita tráfico HTTP y SSH
resource "aws_security_group" "allow_http" {
  name        = "allow_http"
  description = "Allow HTTP and SSH traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "allow_http"
    Description = "Grupo de seguridad que permite tráfico HTTP desde cualquier lugar"
  }
}

# Crear una clave SSH usando TLS para la instancia EC2
resource "tls_private_key" "web_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Crear el key pair en AWS
resource "aws_key_pair" "web_key" {
  key_name   = "web_key"
  public_key = tls_private_key.web_key.public_key_openssh
}

# Crear una instancia EC2 para alojar una aplicación web
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  subnet_id              = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.allow_http.id]
  key_name               = aws_key_pair.web_key.key_name

  tags = {
    Name        = "Web-Instance"
    Description = "Instancia EC2 para alojar una aplicación web"
  }
}

# Recuperar las zonas de disponibilidad para crear recursos en la zona más adecuada
data "aws_availability_zones" "available" {}

# Seleccionar la AMI más reciente de Ubuntu 20.04 LTS
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

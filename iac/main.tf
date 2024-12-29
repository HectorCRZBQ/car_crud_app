provider "aws" {
  region = var.region
}

# Generate SSH Key
resource "tls_private_key" "ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Create AWS Key Pair
resource "aws_key_pair" "web_key" {
  key_name   = "web-app-key"
  public_key = tls_private_key.ssh.public_key_openssh
}

# VPC Configuration (existing code remains the same)
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  
  tags = {
    Name = "Main-VPC"
  }
}

# Update the security group to only allow GitHub Actions IP
resource "aws_security_group" "allow_http" {
  name        = "allow_http"
  description = "Allow HTTP and restricted SSH traffic"
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
    cidr_blocks = [var.github_actions_ip]  # Restrict SSH access
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Add route table for internet access
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "Main Route Table"
  }
}

resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}


# Crear una instancia EC2 para alojar una aplicación web
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  subnet_id              = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.allow_http.id]

  tags = {
    Name = "Web-Instance"
    Description = "Instancia EC2 para alojar una aplicación web"
  }
}

# Recuperar las zonas de disponibilidad para crear recursos en la zona más adecuada
data "aws_availability_zones" "available" {}

# Seleccionar la AMI más reciente de Ubuntu 20.04 LTS
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Ubuntu owner ID
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

# Crear un Network ACL para la VPC
resource "aws_network_acl" "main_acl" {
  vpc_id = aws_vpc.main.id

  # Regla de entrada para permitir tráfico SSH en el puerto 22 desde cualquier fuente
  ingress {
    rule_no       = 100
    protocol      = "tcp"
    from_port     = 22
    to_port       = 22
    cidr_block    = "0.0.0.0/0"  # Permitir desde cualquier IP
    action   = "allow"
  }

  # Regla de entrada para permitir tráfico HTTP en el puerto 80
  ingress {
    rule_no       = 110
    protocol      = "tcp"
    from_port     = 80
    to_port       = 80
    cidr_block    = "0.0.0.0/0"  # Permitir tráfico HTTP desde cualquier fuente
    action   = "allow"
  }

  # Regla de salida para permitir todo el tráfico de salida
  egress {
    rule_no       = 100
    protocol      = "tcp"
    from_port     = 0
    to_port       = 0
    cidr_block    = "0.0.0.0/0"  # Permitir salida a cualquier dirección
    action   = "allow"
  }

  # Regla de salida para denegar todo el tráfico si no está especificado
  egress {
    rule_no       = 200
    protocol      = "tcp"
    from_port     = 0
    to_port       = 0
    cidr_block    = "0.0.0.0/0"
    action   = "deny"
  }
}

# Asociar el NACL con la subred
resource "aws_network_acl_association" "main_acl_association" {
  network_acl_id = aws_network_acl.main_acl.id
  subnet_id      = aws_subnet.main.id
}

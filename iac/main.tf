provider "aws" {
  region = var.region
}

# Crear VPC principal
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "Main-VPC"
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
    Name = "Main-Subnet"
    Description = "Subred pública asociada a la VPC principal"
  }
}

# Crear una puerta de enlace de Internet para la VPC
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "Main-IGW"
    Description = "Puerta de enlace de Internet para la VPC"
  }
}

# Crear un grupo de seguridad que permita tráfico HTTP
resource "aws_security_group" "allow_http" {
  name        = "allow_http"
  description = "Allow HTTP traffic"
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
    cidr_blocks = ["0.0.0.0/0"]  # Asegúrate de que sea accesible desde GitHub Actions o tu IP local
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_http"
    Description = "Grupo de seguridad que permite tráfico HTTP desde cualquier lugar"
  }
}

# Crear una clave SSH para la instancia EC2
resource "aws_key_pair" "web_key" {
  key_name   = "web-key"
  public_key = file("~/.ssh/id_rsa.pub")  # Asegúrate de tener tu clave pública aquí
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

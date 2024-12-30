# Salida con la IP pública de la instancia EC2
output "instance_public_ip" {
  description = "Dirección IP pública de la instancia EC2"
  value       = aws_instance.web.public_ip
}

# Salida con el ID de la VPC creada
output "vpc_id" {
  description = "ID de la VPC principal creada"
  value       = aws_vpc.main.id
}

# Salida con el ID de la subred creada
output "subnet_id" {
  description = "ID de la subred pública creada"
  value       = aws_subnet.main.id
}

# Output de la clave privada para usarla en el pipeline
output "private_key" {
  value       = tls_private_key.web_key.private_key_pem
  sensitive   = true
  description = "Clave PEM privada generada por Terraform"
}

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

output "instance_public_ip" {
  description = "Public IP of EC2 instance"
  value       = aws_instance.web.public_ip
}

output "private_key" {
  description = "Private key for SSH access"
  value       = tls_private_key.ssh.private_key_pem
  sensitive   = true
}
output "instance_id" {
  description = "ID instanta EC2"
  value       = aws_instance.environment_builder.id
}

output "public_ip" {
  description = "Adresa IP Publica a serverului Environment Builder"
  value       = aws_instance.environment_builder.public_ip
}

output "public_dns" {
  description = "Nume DNS Public al serverului Environment Builder"
  value       = aws_instance.environment_builder.public_dns
}

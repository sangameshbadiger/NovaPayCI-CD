output "vpc_id" {
  description = "NovaPay VPC ID"
  value       = aws_vpc.novapay_vpc.id
}

output "subnet_id" {
  description = "NovaPay public subnet ID"
  value       = aws_subnet.novapay_public_subnet.id
}

output "security_group_id" {
  description = "NovaPay security group ID"
  value       = aws_security_group.novapay_sg.id
}

output "ec2_instance_id" {
  description = "NovaPay EC2 instance ID"
  value       = aws_instance.novapay_ec2.id
}

output "ec2_public_ip" {
  description = "NovaPay EC2 public IP"
  value       = aws_instance.novapay_ec2.public_ip
}
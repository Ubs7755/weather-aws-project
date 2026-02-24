output "ec2_public_ip" {
  value = aws_eip.weather_eip.public_ip
}

output "ecr_repository_url" {
  value = aws_ecr_repository.weather_app.repository_url
}

output "ssh_command" {
  value = "ssh -i ~/.ssh/weather-app-key ubuntu@${aws_eip.weather_eip.public_ip}"
}
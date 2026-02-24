terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "weather-app-tfstate-550663032986"
    key    = "weather-app/terraform.tfstate"
    region = "ap-south-1"
  }
}

provider "aws" {
  region = var.region
}

# ECR Repository
resource "aws_ecr_repository" "weather_app" {
  name                 = var.app_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Key Pair for SSH
resource "aws_key_pair" "weather_key" {
  key_name   = "weather-app-key"
  public_key = file("~/.ssh/weather-app-key.pub")
}

# Security Group
resource "aws_security_group" "weather_sg" {
  name        = "weather-app-sg"
  description = "Security group for weather app"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "weather_app" {
  ami                    = "ami-0f58b397bc5c1f2e8"
  instance_type          = var.instance_type
  key_name               = aws_key_pair.weather_key.key_name
  vpc_security_group_ids = [aws_security_group.weather_sg.id]

  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io awscli
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ubuntu
  EOF

  tags = {
    Name        = var.app_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# Elastic IP
resource "aws_eip" "weather_eip" {
  instance = aws_instance.weather_app.id
  domain   = "vpc"
}
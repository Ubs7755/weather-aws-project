# 🌤️ Weather Dashboard - AWS DevOps Project

A production-style DevOps project deploying a Python Flask weather application on AWS using Docker, Terraform, and GitHub Actions CI/CD pipeline.

## 🌍 Live Demo
```
http://52.66.181.91:5000
```

## 🏗️ Architecture
```
Developer → GitHub → GitHub Actions CI/CD
                          ↓
                    Build Docker Image
                          ↓
                    Push to AWS ECR
                          ↓
                    Deploy to AWS EC2
                          ↓
                    Live on Internet
```

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| Python Flask | Web application |
| Gunicorn | Production WSGI server |
| Docker | Containerization |
| AWS EC2 | Cloud server (t2.micro - Free Tier) |
| AWS ECR | Private Docker image registry |
| AWS S3 | Remote Terraform state storage |
| Terraform | Infrastructure as Code |
| GitHub Actions | CI/CD Pipeline |
| OpenWeatherMap API | Real-time weather data |

## 📁 Project Structure
```
weather-aws-project/
├── app/
│   ├── app.py              # Flask weather application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container configuration
├── terraform/
│   ├── main.tf             # AWS infrastructure
│   ├── variables.tf        # Input variables
│   └── outputs.tf          # Output values
├── .github/
│   └── workflows/
│       └── deploy.yml      # CI/CD pipeline
└── README.md
```

## ☁️ AWS Infrastructure (Terraform)

Terraform provisions the following AWS resources:

- **EC2 Instance** — t2.micro (Free Tier) running Ubuntu
- **Security Group** — allows ports 22 (SSH), 80 (HTTP), 5000 (App)
- **Elastic IP** — fixed public IP address
- **ECR Repository** — stores Docker images
- **S3 Bucket** — stores Terraform state remotely
- **Key Pair** — SSH access to EC2

## 🚀 CI/CD Pipeline

Every push to `main` branch automatically:

1. Checks out code
2. Configures AWS credentials
3. Logs into AWS ECR
4. Builds Docker image
5. Tags and pushes image to ECR
6. SSHs into EC2 and pulls latest image
7. Restarts container with zero downtime

## 🔧 Local Setup

### Prerequisites
- Docker Desktop
- Terraform
- AWS CLI configured
- Git Bash / WSL2

### Run Locally
```bash
# Clone the repo
git clone https://github.com/Ubs7755/weather-aws-project.git
cd weather-aws-project

# Run with Docker
docker build -t weather-app:v1 ./app
docker run -d -p 5000:5000 \
  -e WEATHER_API_KEY=your_api_key \
  weather-app:v1

# Open browser
http://localhost:5000
```

### Deploy to AWS
```bash
# Provision infrastructure
cd terraform
terraform init
terraform apply -var="weather_api_key=your_api_key"

# Push image to ECR
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin your_ecr_url
docker tag weather-app:v1 your_ecr_url:v1
docker push your_ecr_url:v1
```

## 🔐 GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `ECR_REPOSITORY_URL` | AWS ECR repository URL |
| `EC2_HOST` | EC2 public IP address |
| `EC2_SSH_KEY` | Private SSH key for EC2 |
| `WEATHER_API_KEY` | OpenWeatherMap API key |

## 📊 Features

- Real-time weather data for any city worldwide
- Temperature, humidity, wind speed, feels like
- Production-grade Gunicorn server
- Auto-restart on container/server failure
- Automated deployments on every code push

## ⚠️ Cost Management

This project uses AWS Free Tier:
- EC2 t2.micro — 750 hrs/month free
- S3 — 5GB free
- ECR — 500MB/month free

Stop EC2 when not in use:
```bash
aws ec2 stop-instances --instance-ids your_instance_id --region ap-south-1
```

## 🎯 What I Learned

- Containerizing Python apps with Docker and Gunicorn
- Provisioning AWS infrastructure with Terraform
- Managing remote Terraform state on S3
- Pushing Docker images to AWS ECR
- Deploying and managing apps on EC2
- Writing production CI/CD pipelines with GitHub Actions
- AWS IAM permissions and security best practices
- SSH key-based authentication for cloud servers
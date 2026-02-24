variable "region" {
  default = "ap-south-1"
}

variable "app_name" {
  default = "weather-app"
}

variable "environment" {
  default = "production"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "weather_api_key" {
  description = "OpenWeatherMap API key"
  type        = string
  sensitive   = true
}
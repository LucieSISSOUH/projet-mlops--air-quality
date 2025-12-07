// tofu/variables.tf

variable "aws_region" {
  description = "AWS default region (e.g., eu-west-3)"
  type        = string
  default     = "eu-west-3"
}

variable "ssh_public_key_path" {
  description = "Path to the local SSH public key (e.g., ~/.ssh/myKeyML.pub)"
  type        = string
}

variable "ssh_private_key_path" {
  description = "Path to the local SSH private key (e.g., ~/.ssh/myKeyML.pem)"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type (t2.micro or t3.micro)"
  type        = string
  // CORRECTION : Changer pour t3.micro pour l'éligibilité Free Tier
  default     = "t3.micro" 
}

variable "api_port" {
  description = "Port for the API (Flask/FastAPI)"
  type        = number
  default     = 8000
}

variable "grafana_port" {
  description = "Port for Grafana"
  type        = number
  default     = 3000
}

variable "grafana_password" {
  description = "Admin password for Grafana"
  type        = string
  default     = "admin123" 
}
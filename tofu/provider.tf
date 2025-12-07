// tofu/providers.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4" 
    }
    template = {
      source  = "hashicorp/template"
      version = "~> 2.2"
    }
  }
}

// Utilise la région définie dans variables.tf (lue depuis le .env)
provider "aws" {
  region = var.aws_region
}
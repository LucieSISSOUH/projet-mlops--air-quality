// tofu/outputs.tf

output "api_ip" {
  description = "Public IP address of the API instance"
  value       = aws_instance.api_instance.public_ip
}

output "monitoring_ip" {
  description = "Public IP address of the monitoring instance"
  value       = aws_instance.monitoring_instance.public_ip
}

output "api_url" {
  description = "URL to access the prediction API"
  value       = "http://${aws_instance.api_instance.public_ip}:${var.api_port}"
}

output "grafana_url" {
  description = "URL to access the Grafana dashboard"
  value       = "http://${aws_instance.monitoring_instance.public_ip}:${var.grafana_port}"
}
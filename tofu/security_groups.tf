// Fichier : tofu/security_groups.tf

// --- Security Group pour l'Instance API ---
resource "aws_security_group" "sg_api" {
  name        = "mlops-api-sg"
  description = "Allow SSH, API (port 8000) and Metrics (port 9090) access"

  // 1. SSH (port 22) - Acces general
  ingress {
    description = "Acces SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  // 2. API Publique (Port 8000) - Acces general
  ingress {
    description = "Acces public a l API MLOps"
    from_port   = 8000 // Port fixé
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  // 3. Metriques Prometheus (Port 9090) - Acces limite a l'instance de monitoring
  ingress {
    description = "Acces aux metriques 9090 depuis monitoring"
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    // Limite l'acces a l'IP PRIVE de l'instance de monitoring
    cidr_blocks = ["46.193.64.220/32"] 
  }

  // Trafic sortant illimite
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

// --- Security Group pour l'Instance Monitoring (Prometheus/Grafana) ---
resource "aws_security_group" "sg_monitoring" {
  name        = "mlops-monitoring-sg"
  description = "Allow SSH and Grafana access"

  // 1. SSH (port 22) - Acces general
  ingress {
    description = "Acces SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  // 2. Grafana (port 3000 par defaut) - Acces general
  ingress {
    description = "Acces a l interface Grafana"
    from_port   = var.grafana_port
    to_port     = var.grafana_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  // Trafic sortant illimite
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
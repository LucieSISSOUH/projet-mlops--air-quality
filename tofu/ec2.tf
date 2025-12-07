// tofu/ec2.tf

// Instance pour l'API (t2.micro)
resource "aws_instance" "api_instance" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  // Attache la Key Pair importée
  key_name      = aws_key_pair.mlops_keypair.key_name 
  vpc_security_group_ids = [aws_security_group.sg_api.id] 

  tags = {
    Name = "MLOps-API-Instance"
  }
}

// Instance pour le Monitoring (t2.micro)
resource "aws_instance" "monitoring_instance" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  // Attache la Key Pair importée
  key_name      = aws_key_pair.mlops_keypair.key_name 
  vpc_security_group_ids = [aws_security_group.sg_monitoring.id] 

  tags = {
    Name = "MLOps-Monitoring-Instance"
  }
}
// Fichier : tofu/inventory.tf

// 1. Génération de l'inventaire Ansible (fichier local)
resource "local_file" "ansible_inventory" {
  // Chemin de destination pour Ansible
  filename = "../ansible/inventory.yml" 
  
  // Utilise le modèle inventory.tpl (correction du chemin)
  content  = templatefile("${path.module}/templates/inventory.tpl", {
    
    // --- Variables de Connexion et de Sécurité ---
    ssh_private_key_path = var.ssh_private_key_path,
    grafana_password     = var.grafana_password,

    // --- Variables d'IP publiques des instances (CORRIGÉ) ---
    // La clé 'api_ip' est celle qu'attend le modèle inventory.tpl
    api_ip        = aws_instance.api_instance.public_ip, 
    monitoring_ip = aws_instance.monitoring_instance.public_ip,

    // --- Variables de Ports FIXÉES ---
    api_port      = 8000,      // Port de l'API (8000)
    grafana_port  = 3000,      // Port de Grafana (3000)
    
  })
}
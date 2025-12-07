// tofu/templates/inventory.tpl

all:
  vars:
    ansible_user: ubuntu
    # Ansible a besoin de la clé PRIVÉE (myKeyML.pem) pour se connecter aux instances EC2.
    ansible_ssh_private_key_file: ${ssh_private_key_path}
    # Mot de passe pour la configuration initiale de Grafana (lu depuis variables.tf)
    grafana_password: ${grafana_password} 
  children:
    # Groupe pour l'instance API
    api_group:
      hosts:
        api_host:
          # IP de l'instance API fournie par OpenTofu
          ansible_host: ${api_ip} 
          api_port: ${api_port}
    
    # Groupe pour l'instance Monitoring
    monitoring_group:
      hosts:
        monitoring_host:
          # IP de l'instance Monitoring fournie par OpenTofu
          ansible_host: ${monitoring_ip}
          grafana_port: ${grafana_port}
          # URL complète de l'API cible pour la configuration de Prometheus par Ansible
          api_target: http://${api_ip}:${api_port}
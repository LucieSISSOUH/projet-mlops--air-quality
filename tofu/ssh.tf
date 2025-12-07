// tofu/ssh.tf

// Lit le contenu de votre clé publique locale (e.g., ~/.ssh/myKeyML.pub)
data "local_file" "public_key" {
  filename = var.ssh_public_key_path
}

// 2. Crée la Key Pair sur AWS sous un nouveau nom unique
resource "aws_key_pair" "mlops_keypair" {
  key_name   = "myKeyMLOps" // <-- NOM UNIQUE POUR ÉVITER LE CONFLIT
  public_key = data.local_file.public_key.content
}
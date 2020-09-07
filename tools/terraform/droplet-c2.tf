resource "digitalocean_droplet" "c2" {
  image = "ubuntu-20-04-x64"
  name = "c2"
  region = "sfo2"
  size = "c-8"
  private_networking = true
  ssh_keys = [
    data.digitalocean_ssh_key.key1.id,
    data.digitalocean_ssh_key.key2.id
  ]
  connection {
    host = self.ipv4_address
    user = "root"
    type = "ssh"
    private_key = file(var.pvt_key)
    timeout = "2m"
  }
#  provisioner "remote-exec" {
#    inline = [
#      "export PATH=$PATH:/usr/bin",
#      "sudo apt-get update",
#      "sudo apt-get -y install vim git nmap"
#    ]
#  }
}

resource "digitalocean_project_resources" "ctf" {
  project = data.digitalocean_project.ctf.id
  resources = [
    digitalocean_droplet.c2.urn
  ]
}

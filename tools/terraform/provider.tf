terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "1.22.2"
    }
  }
}

variable "do_token" {}
variable "pvt_key" {}

provider "digitalocean" {
  token = var.do_token
}

data "digitalocean_ssh_key" "key1" {
  name = "key1"
}
data "digitalocean_ssh_key" "key2" {
  name = "key2"
}

data "digitalocean_project" "ctf" {
  id = "0603c8a4-0bfe-4c21-a551-affa9d29bf65"
}

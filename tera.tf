provider "google" {
  credentials = file("kubernetes-390002-4f61bddcfd62.json")
  project     = "kubernetes-390002"
  region      = "us-central1"
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}
resource "google_container_cluster" "my-cluster" {
  name               = "my-cluster1"
  location           = "us-central1-a"
  remove_default_node_pool = true
  initial_node_count = 1

  master_auth {
    username = ""
    password = ""
  }
}

resource "google_container_node_pool" "my-node-pool" {
  name       = "my-node-pool"
  location   = "us-central1-a"
  cluster    = google_container_cluster.my-cluster.name
  node_count = 1

  node_config {
    machine_type = "e2-medium"
    disk_size_gb = 50

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}

output "kubeconfig" {
  value = <<-EOT
    apiVersion: v1
    clusters:
    - cluster:
        certificate-authority-data: ${google_container_cluster.my-cluster.master_auth[0].cluster_ca_certificate}
        server: https://${google_container_cluster.my-cluster.endpoint}
      name: my-cluster
    contexts:
    - context:
        cluster: my-cluster
        user: my-user
      name: my-context
    current-context: my-context
    kind: Config
    preferences: {}
    users:
    - name: my-user
      user:
        auth-provider:
          config:
            cmd-args: config config-helper --format=json
            cmd-path: gcloud
            expiry-key: '{.credential.token_expiry}'
            token-key: '{.credential.access_token}'
          name: gcp
  EOT
}
terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# GCS for MLflow artifacts
resource "google_storage_bucket" "mlflow_artifacts" {
  name          = "${var.project_id}-mlflow-artifacts"
  location      = var.region
  force_destroy = true
}

# Artifact Registry for Docker images
resource "google_artifact_registry_repository" "api_repo" {
  location      = var.region
  repository_id = "asfotec-mlstack"
  format        = "DOCKER"
  description   = "API Docker images"
}

# Cloud Run service
resource "google_cloud_run_service" "api" {
  name     = "asfotec-mlstack-api"
  location = var.region

  template {
    spec {
      containers {
        image = "${var.artifact_registry_repo}/${var.image_name}:latest"
        ports {
          container_port = 8080
        }
        env {
          name  = "PORT"
          value = "8080"
        }
        # Add other envs from secrets
        resources {
          limits = {
            cpu    = "1000m"
            memory = "1Gi"
          }
        }
      }
      # Scale to zero
      timeout_seconds = 300
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  autogenerate_revision_name = true
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.api.location
  project     = google_cloud_run_service.api.project
  service     = google_cloud_run_service.api.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

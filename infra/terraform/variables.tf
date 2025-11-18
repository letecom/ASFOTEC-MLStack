variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "europe-west1"
}

variable "artifact_registry_repo" {
  description = "Artifact Registry repo URL"
  type        = string
  default     = "europe-west1-docker.pkg.dev/PROJECT_ID/asfotec-mlstack"
}

variable "image_name" {
  description = "Docker image name"
  type        = string
  default     = "api"
}

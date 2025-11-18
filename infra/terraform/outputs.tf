output "cloud_run_url" {
  value = google_cloud_run_service.api.status[0].url
}

output "gcs_bucket" {
  value = google_storage_bucket.mlflow_artifacts.name
}

output "knowledge_bucket_name" {
  value = google_storage_bucket.knowledge_bucket.name
}

output "bigquery_dataset_id" {
  value = google_bigquery_dataset.fraud_dataset.dataset_id
}

output "pubsub_topic_name" {
  value = google_pubsub_topic.transactions_topic.name
}

output "agent_service_account_email" {
  value = google_service_account.agent_sa.email
}

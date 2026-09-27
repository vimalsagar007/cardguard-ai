# Terraform Configuration for CardGuard AI - Dev Environment

terraform {
  required_version = ">= 1.5.0"
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

# 1. Cloud Storage Bucket for RAG Knowledge
resource "google_storage_bucket" "knowledge_bucket" {
  name                     = "cardguard-knowledge-${var.environment}-${var.project_id}"
  location                 = var.region
  force_destroy            = true
  public_access_prevention = "enforced"

  uniform_bucket_level_access = true
}

# 2. BigQuery Dataset & Tables
resource "google_bigquery_dataset" "fraud_dataset" {
  dataset_id                  = "cardguard_fraud_db_${var.environment}"
  friendly_name               = "CardGuard Fraud DB (${var.environment})"
  description                 = "BigQuery dataset storing transaction logs, employee baselines, and cases"
  location                    = var.region
  default_table_expiration_ms = 3600000000
}

# 3. Pub/Sub Topic for Real-time Transaction Ingestion
resource "google_pubsub_topic" "transactions_topic" {
  name = "cardguard-transactions-ingestion-${var.environment}"
}

resource "google_pubsub_subscription" "transactions_sub" {
  name  = "cardguard-transactions-sub-${var.environment}"
  topic = google_pubsub_topic.transactions_topic.name

  ack_deadline_seconds = 20
}

# 4. Secret Manager for API Keys & Tokens
resource "google_secret_manager_secret" "mcp_token_secret" {
  secret_id = "cardguard-mcp-token-${var.environment}"
  replication {
    auto {}
  }
}

# 5. Service Account for Agent Runtime
resource "google_service_account" "agent_sa" {
  account_id   = "cardguard-agent-sa-${var.environment}"
  display_name = "CardGuard AI Agent Runtime Service Account"
}

# 6. Artifact Registry Repository
resource "google_artifact_registry_repository" "cardguard_repo" {
  location      = var.region
  repository_id = "cardguard-ai-repo-${var.environment}"
  description   = "Docker repository for CardGuard AI Cloud Run services"
  format        = "DOCKER"
}

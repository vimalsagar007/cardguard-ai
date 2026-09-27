variable "project_id" {
  type        = string
  description = "GCP Project ID"
  default     = "cardguard-ai-dev-project"
}

variable "region" {
  type        = string
  description = "GCP Region"
  default     = "us-central1"
}

variable "environment" {
  type        = string
  description = "Deployment environment (dev, test, prod)"
  default     = "dev"
}

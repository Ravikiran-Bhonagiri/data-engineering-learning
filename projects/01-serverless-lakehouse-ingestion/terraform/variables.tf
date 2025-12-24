variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project identifier used for naming resources"
  type        = string
  default     = "serverless-lakehouse"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "catalog_name" {
  description = "Unity Catalog name to bind resources to"
  type        = string
  default     = "p1_log_ingest"
}

variable "databricks_account_id" {
  description = "Databricks AWS Account ID for IAM Trust Policy"
  type        = string
  # Replace with actual Databricks ID from your Unity Catalog setup
  default     = "414351767826" 
}

output "landing_bucket" {
  description = "Name of the Landing Zone bucket"
  value       = aws_s3_bucket.landing.id
}

output "bronze_bucket" {
  description = "Name of the Bronze Layer bucket"
  value       = aws_s3_bucket.bronze.id
}

output "silver_bucket" {
  description = "Name of the Silver Layer bucket"
  value       = aws_s3_bucket.silver.id
}

output "gold_bucket" {
  description = "Name of the Gold Layer bucket"
  value       = aws_s3_bucket.gold.id
}

resource "aws_s3_bucket" "landing_zone" {
  bucket = "${var.project_name}-${var.environment}-landing-zone"

  tags = {
    Name        = "Landing Zone"
    Environment = var.environment
    Project     = var.project_name
    Layer       = "Landing"
  }
}

resource "aws_s3_bucket" "bronze" {
  bucket = "${var.project_name}-${var.environment}-bronze"

  tags = {
    Name        = "Bronze Layer"
    Environment = var.environment
    Project     = var.project_name
    Layer       = "Bronze"
  }
}

resource "aws_s3_bucket" "silver" {
  bucket = "${var.project_name}-${var.environment}-silver"

  tags = {
    Name        = "Silver Layer"
    Environment = var.environment
    Project     = var.project_name
    Layer       = "Silver"
  }
}

# Versioning is good practice for Data Lakes
resource "aws_s3_bucket_versioning" "landing_ver" {
  bucket = aws_s3_bucket.landing_zone.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "bronze_ver" {
  bucket = aws_s3_bucket.bronze.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Create a folder structure placeholder (optional, but helpful visualize)
resource "aws_s3_object" "logs_folder" {
  bucket = aws_s3_bucket.landing_zone.id
  key    = "app_logs/"
  source = "/dev/null" # Placeholder
}

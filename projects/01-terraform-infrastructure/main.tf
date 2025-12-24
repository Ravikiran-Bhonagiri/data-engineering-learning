provider "aws" {
  region = var.aws_region
}

# ==========================================
# 1. Landing Zone (Transient)
# ==========================================
resource "aws_s3_bucket" "landing" {
  bucket = "${var.project_prefix}-${var.env}-landing"
  
  tags = {
    Name        = "Landing Zone"
    Environment = var.env
    Layer       = "Landing"
  }
}

resource "aws_s3_bucket_public_access_block" "landing_block" {
  bucket = aws_s3_bucket.landing.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ==========================================
# 2. Bronze Layer (Raw History)
# ==========================================
resource "aws_s3_bucket" "bronze" {
  bucket = "${var.project_prefix}-${var.env}-bronze"

  tags = {
    Layer = "Bronze"
  }
}

resource "aws_s3_bucket_versioning" "bronze_ver" {
  bucket = aws_s3_bucket.bronze.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bronze_enc" {
  bucket = aws_s3_bucket.bronze.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "bronze_block" {
  bucket = aws_s3_bucket.bronze.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ==========================================
# 3. Silver Layer (Cleaned)
# ==========================================
resource "aws_s3_bucket" "silver" {
  bucket = "${var.project_prefix}-${var.env}-silver"
  tags = { Layer = "Silver" }
}

resource "aws_s3_bucket_versioning" "silver_ver" {
  bucket = aws_s3_bucket.silver.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_public_access_block" "silver_block" {
  bucket = aws_s3_bucket.silver.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ==========================================
# 4. Gold Layer (Business Aggregates)
# ==========================================
resource "aws_s3_bucket" "gold" {
  bucket = "${var.project_prefix}-${var.env}-gold"
  tags = { Layer = "Gold" }
}

resource "aws_s3_bucket_versioning" "gold_ver" {
  bucket = aws_s3_bucket.gold.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_public_access_block" "gold_block" {
  bucket = aws_s3_bucket.gold.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

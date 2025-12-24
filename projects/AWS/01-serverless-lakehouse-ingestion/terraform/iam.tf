# IAM Role for Unity Catalog to access S3
resource "aws_iam_role" "unity_catalog_role" {
  name = "${var.project_name}-uc-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${var.databricks_account_id}:root"
        }
        Condition = {
          StringEquals = {
            "sts:ExternalId" = var.databricks_account_id
          }
        }
      }
    ]
  })
}

# Policy allowing access to our specific buckets
resource "aws_iam_policy" "unity_catalog_policy" {
  name        = "${var.project_name}-uc-policy"
  description = "Allow Unity Catalog to access serverless lakehouse buckets"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ]
        Effect = "Allow"
        Resource = [
          aws_s3_bucket.landing_zone.arn,
          "${aws_s3_bucket.landing_zone.arn}/*",
          aws_s3_bucket.bronze.arn,
          "${aws_s3_bucket.bronze.arn}/*",
          aws_s3_bucket.silver.arn,
          "${aws_s3_bucket.silver.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "uc_attach" {
  role       = aws_iam_role.unity_catalog_role.name
  policy_arn = aws_iam_policy.unity_catalog_policy.arn
}

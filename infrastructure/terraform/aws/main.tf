terraform {
  required_version = ">= 1.6.0"
}

# Intentionally provider-neutral for the portfolio starter.
# AWS modules will be added in the platform phase for EKS, networking,
# PostgreSQL and observability infrastructure.

variable "environment" {
  type    = string
  default = "qa"
}

output "environment" {
  value = var.environment
}

terraform {
  required_version = ">= 0.10.7"
}

provider "aws" {
  region = "eu-west-1"
  profile = "devo"
}
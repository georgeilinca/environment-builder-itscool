variable "aws_region" {
  description = "Regiunea AWS in care va fi creat env"
  type        = string
  default     = "eu-central-1"
}

variable "instance_type" {
  description = "Tipul instantei EC2"
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "ID AMI Ubuntu pentru instanta EC2"
  type        = string
}

variable "key_name" {
  description = "Nume pereche chei existente EC2"
  type        = string
}

variable "ssh_allowed_cidr" {
  description = "CIDR permis sa acceseze SSH"
  type        = string
  default     = "0.0.0.0/0"
}

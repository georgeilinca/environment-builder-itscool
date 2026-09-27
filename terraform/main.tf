data "aws_vpc" "default" {
  default = true
}

resource "aws_subnet" "environment_builder" {
  vpc_id                  = data.aws_vpc.default.id
  cidr_block              = "172.31.10.0/24"
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = true

  tags = {
    Name    = "environment-builder-subnet"
    Project = "environment-builder"
  }
}

data "aws_internet_gateway" "default" {
  filter {
    name   = "attachment.vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_route_table" "environment_builder" {
  vpc_id = data.aws_vpc.default.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = data.aws_internet_gateway.default.id
  }

  tags = {
    Name    = "environment-builder-route-table"
    Project = "environment-builder"
  }
}

resource "aws_route_table_association" "environment_builder" {
  subnet_id      = aws_subnet.environment_builder.id
  route_table_id = aws_route_table.environment_builder.id
}

resource "aws_security_group" "environment_builder" {
  name        = "environment-builder-sg"
  description = "Security group pentru server Environment Builder"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  egress {
    description = "Permite trafic extern"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "environment-builder-sg"
    Project = "environment-builder"
  }
}

resource "aws_instance" "environment_builder" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.environment_builder.id
  key_name                    = var.key_name
  vpc_security_group_ids      = [aws_security_group.environment_builder.id]
  associate_public_ip_address = true

  tags = {
    Name    = "environment-builder-server"
    Project = "environment-builder"
  }
}
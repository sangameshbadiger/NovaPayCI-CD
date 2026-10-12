resource "aws_vpc" "novapay_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "novapay-vpc"
    Project     = "NovaPay"
    Environment = "dev"
  }
}

resource "aws_subnet" "novapay_public_subnet" {
  vpc_id                  = aws_vpc.novapay_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = false

  tags = {
    Name        = "novapay-public-subnet"
    Project     = "NovaPay"
    Environment = "dev"
  }
}

resource "aws_internet_gateway" "novapay_igw" {
  vpc_id = aws_vpc.novapay_vpc.id

  tags = {
    Name        = "novapay-igw"
    Project     = "NovaPay"
    Environment = "dev"
  }
}

resource "aws_route_table" "novapay_public_rt" {
  vpc_id = aws_vpc.novapay_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.novapay_igw.id
  }

  tags = {
    Name        = "novapay-public-rt"
    Project     = "NovaPay"
    Environment = "dev"
  }
}

resource "aws_route_table_association" "novapay_public_assoc" {
  subnet_id      = aws_subnet.novapay_public_subnet.id
  route_table_id = aws_route_table.novapay_public_rt.id
}

resource "aws_security_group" "novapay_sg" {
  name        = "novapay-sg"
  description = "Security group for NovaPay application"
  vpc_id      = aws_vpc.novapay_vpc.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["103.186.41.37/32"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Outbound traffic for application operations"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "novapay-sg"
    Project     = "NovaPay"
    Environment = "dev"
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}

resource "aws_instance" "novapay_ec2" {
  ebs_optimized               = true
  monitoring                  = true
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = "t3.micro"
  key_name                    = "RSA"
  iam_instance_profile        = "NovaPayEC2ECRRole"
  subnet_id                   = aws_subnet.novapay_public_subnet.id
  vpc_security_group_ids      = [aws_security_group.novapay_sg.id]
  associate_public_ip_address = true

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  root_block_device {
    encrypted = true
  }

  user_data = file("${path.module}/user_data.sh")

  user_data_replace_on_change = true

  tags = {
    Name        = "novapay-ec2"
    Project     = "NovaPay"
    Environment = "dev"
  }
}
resource "aws_default_security_group" "novapay_default_sg" {
  vpc_id = aws_vpc.novapay_vpc.id

  ingress = []
  egress  = []

  tags = {
    Name        = "novapay-default-sg-restricted"
    Project     = "NovaPay"
    Environment = "dev"
  }
}

resource "aws_flow_log" "novapay_vpc_flow_logs" {
  vpc_id               = aws_vpc.novapay_vpc.id
  traffic_type         = "ALL"
  log_destination_type = "cloud-watch-logs"
  log_destination      = "arn:aws:logs:ap-south-1:570064633022:log-group:/novapay/vpc-flow-logs"
  iam_role_arn         = "arn:aws:iam::570064633022:role/service-role/NovaPayVPCFlowLogsRole"

  max_aggregation_interval = 600

  tags = {
    Name        = "novapay-vpc-flow-logs"
    Project     = "NovaPay"
    Environment = "dev"
  }
}

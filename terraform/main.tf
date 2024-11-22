# Create VPC
resource "aws_vpc" "flashcards_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "flashcards-vpc"
  }
}

# Create two subnets in different availability zones
resource "aws_subnet" "flashcards_subnet_1" {
  vpc_id                  = aws_vpc.flashcards_vpc.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "fc-pub-subnet-1"
  }
}

resource "aws_subnet" "flashcards_subnet_2" {
  vpc_id                  = aws_vpc.flashcards_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
  tags = {
    Name = "fc-pub-subnet-2"
  }
}

# Create an Internet Gateway (needed for public subnets to communicate with the internet)
resource "aws_internet_gateway" "flashcards_igw" {
  vpc_id = aws_vpc.flashcards_vpc.id
  tags = {
    Name = "flashcards-igw"
  }
}

# Create a Route Table
resource "aws_route_table" "flashcards_route_table" {
  vpc_id = aws_vpc.flashcards_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.flashcards_igw.id
  }
}

# Associate subnets with the route table
resource "aws_route_table_association" "flashcards_subnet_1_association" {
  subnet_id      = aws_subnet.flashcards_subnet_1.id
  route_table_id = aws_route_table.flashcards_route_table.id
}

resource "aws_route_table_association" "flashcards_subnet_2_association" {
  subnet_id      = aws_subnet.flashcards_subnet_2.id
  route_table_id = aws_route_table.flashcards_route_table.id
}

# Create Security Group for ECS
resource "aws_security_group" "flashcards_sg" {
  name        = "fc-security-group"
  description = "Allow traffic to Flask app"
  vpc_id      = aws_vpc.flashcards_vpc.id

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create ECS Cluster
resource "aws_ecs_cluster" "flashcards_cluster" {
  name = "flashcards-cluster"
}

# Create ECR Repository for Docker images
resource "aws_ecr_repository" "flashcards_repo" {
  name = "flashcards-app-repo"
}

# IAM roles for ECS execution and task
resource "aws_iam_role" "ecs_execution_role" {
  name = "ecsExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
      Effect = "Allow"
      Sid    = ""
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy" 
  role       = aws_iam_role.ecs_execution_role.name
}

resource "aws_iam_role" "ecs_task_role" {
  name = "ecsTaskRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
      Effect = "Allow"
      Sid    = ""
    }]
  })
}

# ECS Task Definition
resource "aws_ecs_task_definition" "flashcards_task" {
  family                   = "flashcards-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([{
    name      = "flashcards-container"
    image     = "${aws_ecr_repository.flashcards_repo.repository_url}:latest"
    essential = true
    portMappings = [{
      containerPort = 5000
      hostPort      = 5000
      protocol      = "tcp"
    }]
  }])
}

# ECS Service
resource "aws_ecs_service" "flashcards_service" {
  name            = "flashcards-service"
  cluster         = aws_ecs_cluster.flashcards_cluster.id
  task_definition = aws_ecs_task_definition.flashcards_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.flashcards_subnet_1.id, aws_subnet.flashcards_subnet_2.id]
    security_groups = [aws_security_group.flashcards_sg.id]
    assign_public_ip = true
  }
}
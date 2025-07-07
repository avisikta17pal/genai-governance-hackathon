#!/bin/bash

# AWS Deployment Script for GenAI Governance System
# This script provides multiple deployment options for AWS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="genai-governance-system"
REGION="us-east-1"
EC2_INSTANCE_TYPE="t3.medium"
ECS_CLUSTER_NAME="genai-governance-cluster"
LAMBDA_FUNCTION_NAME="genai-governance-api"

echo -e "${GREEN}🚀 AWS Deployment Script for GenAI Governance System${NC}"
echo "=================================================="
    
# Function to check AWS CLI
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}❌ AWS CLI is not installed. Please install it first.${NC}"
        exit 1
    fi
    
    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}❌ AWS credentials not configured. Please run 'aws configure' first.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ AWS CLI and credentials verified${NC}"
}

# Function to build Docker image
build_docker_image() {
    echo -e "${YELLOW}🔨 Building Docker image...${NC}"
    docker build -t $PROJECT_NAME .
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
}

# Function to deploy to EC2
deploy_to_ec2() {
    echo -e "${YELLOW}🖥️  Deploying to EC2...${NC}"
    
    # Create security group
    aws ec2 create-security-group \
        --group-name $PROJECT_NAME-sg \
        --description "Security group for GenAI Governance System" \
        --region $REGION || true
    
    # Add rules to security group
    aws ec2 authorize-security-group-ingress \
        --group-name $PROJECT_NAME-sg \
        --protocol tcp \
        --port 8000 \
        --cidr 0.0.0.0/0 \
        --region $REGION || true
    
    aws ec2 authorize-security-group-ingress \
        --group-name $PROJECT_NAME-sg \
        --protocol tcp \
        --port 22 \
        --cidr 0.0.0.0/0 \
        --region $REGION || true
    
    # Create EC2 instance
    INSTANCE_ID=$(aws ec2 run-instances \
        --image-id ami-0c02fb55956c7d316 \
        --count 1 \
        --instance-type $EC2_INSTANCE_TYPE \
        --key-name your-key-pair \
        --security-groups $PROJECT_NAME-sg \
        --user-data file://scripts/ec2-userdata.sh \
        --region $REGION \
        --query 'Instances[0].InstanceId' \
        --output text)
    
    echo -e "${GREEN}✅ EC2 instance created: $INSTANCE_ID${NC}"
    echo -e "${YELLOW}⏳ Waiting for instance to be running...${NC}"
    
    aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $REGION
    
    # Get public IP
    PUBLIC_IP=$(aws ec2 describe-instances \
        --instance-ids $INSTANCE_ID \
        --region $REGION \
        --query 'Reservations[0].Instances[0].PublicIpAddress' \
        --output text)
    
    echo -e "${GREEN}✅ Deployment URL: http://$PUBLIC_IP:8000${NC}"
    echo -e "${GREEN}✅ Health check: http://$PUBLIC_IP:8000/health${NC}"
}

# Function to deploy to ECS
deploy_to_ecs() {
    echo -e "${YELLOW}🐳 Deploying to ECS...${NC}"
    
    # Create ECR repository
    aws ecr create-repository --repository-name $PROJECT_NAME --region $REGION || true
    
    # Get ECR login token
    aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$REGION.amazonaws.com
    
    # Tag and push image
    ECR_URI=$(aws sts get-caller-identity --query Account --output text).dkr.ecr.$REGION.amazonaws.com/$PROJECT_NAME
    docker tag $PROJECT_NAME:latest $ECR_URI:latest
    docker push $ECR_URI:latest
    
    # Create ECS cluster
    aws ecs create-cluster --cluster-name $ECS_CLUSTER_NAME --region $REGION || true
    
    # Create task definition
    cat > task-definition.json << EOF
                {
    "family": "$PROJECT_NAME",
    "networkMode": "awsvpc",
    "requiresCompatibilities": ["FARGATE"],
    "cpu": "256",
    "memory": "512",
    "executionRoleArn": "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/ecsTaskExecutionRole",
    "containerDefinitions": [
        {
            "name": "$PROJECT_NAME",
            "image": "$ECR_URI:latest",
            "portMappings": [
                {
                    "containerPort": 8000,
                    "protocol": "tcp"
                }
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/$PROJECT_NAME",
                    "awslogs-region": "$REGION",
                    "awslogs-stream-prefix": "ecs"
                }
                    }
                }
            ]
}
EOF
    
    # Register task definition
    aws ecs register-task-definition --cli-input-json file://task-definition.json --region $REGION
    
    # Create service
    aws ecs create-service \
        --cluster $ECS_CLUSTER_NAME \
        --service-name $PROJECT_NAME-service \
        --task-definition $PROJECT_NAME \
        --desired-count 1 \
        --launch-type FARGATE \
        --network-configuration "awsvpcConfiguration={subnets=[subnet-12345678],securityGroups=[sg-12345678],assignPublicIp=ENABLED}" \
        --region $REGION || true
    
    echo -e "${GREEN}✅ ECS service deployed successfully${NC}"
}

# Function to deploy to Lambda
deploy_to_lambda() {
    echo -e "${YELLOW}⚡ Deploying to Lambda...${NC}"
    
    # Create deployment package
    pip install -r requirements.txt -t lambda-package/
    cp -r backend/ lambda-package/
    cd lambda-package && zip -r ../lambda-deployment.zip . && cd ..
    
    # Create Lambda function
    aws lambda create-function \
        --function-name $LAMBDA_FUNCTION_NAME \
        --runtime python3.10 \
        --role arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/lambda-execution-role \
        --handler backend.main.handler \
        --zip-file fileb://lambda-deployment.zip \
        --timeout 30 \
        --memory-size 512 \
        --region $REGION || true
    
    # Update function code
    aws lambda update-function-code \
        --function-name $LAMBDA_FUNCTION_NAME \
        --zip-file fileb://lambda-deployment.zip \
        --region $REGION
    
    echo -e "${GREEN}✅ Lambda function deployed successfully${NC}"
}

# Main deployment logic
main() {
    check_aws_cli
    build_docker_image
    
    echo -e "${YELLOW}Choose deployment option:${NC}"
    echo "1) Deploy to EC2"
    echo "2) Deploy to ECS"
    echo "3) Deploy to Lambda"
    echo "4) Deploy to all (EC2 + ECS + Lambda)"
    
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            deploy_to_ec2
            ;;
        2)
            deploy_to_ecs
            ;;
        3)
            deploy_to_lambda
            ;;
        4)
            deploy_to_ec2
            deploy_to_ecs
            deploy_to_lambda
            ;;
        *)
            echo -e "${RED}❌ Invalid choice${NC}"
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
    echo -e "${YELLOW}📝 Don't forget to update your README with the deployment URLs${NC}"
}

# Run main function
main "$@" 
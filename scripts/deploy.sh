#!/bin/bash

# GenAI Governance System Deployment Script
# This script deploys the system to AWS

set -e

echo "🚀 Starting GenAI Governance System Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="genai-governance-system"
AWS_REGION="us-east-1"
STACK_NAME="${PROJECT_NAME}-stack"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if AWS CLI is installed
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install it first."
        exit 1
    fi
    
    # Check if pip is installed
    if ! command -v pip &> /dev/null; then
        print_error "pip is not installed. Please install it first."
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS credentials are not configured. Please run 'aws configure' first."
        exit 1
    fi
    
    print_status "Prerequisites check passed!"
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    pip install -r requirements.txt
    
    print_status "Dependencies installed successfully!"
}

# Create AWS resources
create_aws_resources() {
    print_status "Creating AWS resources..."
    
    # Create S3 bucket for audit logs
    BUCKET_NAME="${PROJECT_NAME}-audit-logs-$(date +%s)"
    print_status "Creating S3 bucket: $BUCKET_NAME"
    aws s3 mb s3://$BUCKET_NAME --region $AWS_REGION
    
    # Create DynamoDB table
    TABLE_NAME="${PROJECT_NAME}-audit-logs"
    print_status "Creating DynamoDB table: $TABLE_NAME"
    aws dynamodb create-table \
        --table-name $TABLE_NAME \
        --attribute-definitions AttributeName=audit_id,AttributeType=S \
        --key-schema AttributeName=audit_id,KeyType=HASH \
        --billing-mode PAY_PER_REQUEST \
        --region $AWS_REGION
    
    # Wait for table to be created
    print_status "Waiting for DynamoDB table to be active..."
    aws dynamodb wait table-exists --table-name $TABLE_NAME --region $AWS_REGION
    
    print_status "AWS resources created successfully!"
}

# Deploy backend
deploy_backend() {
    print_status "Deploying backend..."
    
    # Create deployment package
    print_status "Creating deployment package..."
    cd backend
    
    # Install dependencies for deployment
    pip install -r ../requirements.txt -t .
    
    # Create ZIP file
    zip -r ../backend-deployment.zip . -x "*.pyc" "__pycache__/*" "tests/*"
    
    cd ..
    
    # Deploy to Lambda (if Lambda function exists)
    if aws lambda get-function --function-name ${PROJECT_NAME}-backend &> /dev/null; then
        print_status "Updating Lambda function..."
        aws lambda update-function-code \
            --function-name ${PROJECT_NAME}-backend \
            --zip-file fileb://backend-deployment.zip \
            --region $AWS_REGION
    else
        print_warning "Lambda function ${PROJECT_NAME}-backend does not exist. Please create it manually or use CloudFormation."
    fi
    
    print_status "Backend deployment completed!"
}

# Deploy frontend
deploy_frontend() {
    print_status "Deploying frontend..."
    
    # Create S3 bucket for frontend
    FRONTEND_BUCKET="${PROJECT_NAME}-frontend-$(date +%s)"
    print_status "Creating S3 bucket for frontend: $FRONTEND_BUCKET"
    aws s3 mb s3://$FRONTEND_BUCKET --region $AWS_REGION
    
    # Configure bucket for static website hosting
    aws s3 website s3://$FRONTEND_BUCKET \
        --index-document index.html \
        --error-document error.html
    
    # Upload frontend files
    print_status "Uploading frontend files..."
    aws s3 sync frontend/ s3://$FRONTEND_BUCKET --region $AWS_REGION
    
    print_status "Frontend deployed successfully!"
    print_status "Frontend URL: http://$FRONTEND_BUCKET.s3-website-$AWS_REGION.amazonaws.com"
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Run backend tests
    cd backend
    python -m pytest tests/ -v
    cd ..
    
    print_status "Tests completed!"
}

# Start local development
start_local() {
    print_status "Starting local development environment..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Start backend
    print_status "Starting backend server..."
    cd backend
    uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..
    
    # Start frontend
    print_status "Starting frontend application..."
    cd frontend
    streamlit run app.py --server.port 8501 &
    FRONTEND_PID=$!
    cd ..
    
    print_status "Local development environment started!"
    print_status "Backend: http://localhost:8000"
    print_status "Frontend: http://localhost:8501"
    print_status "API Docs: http://localhost:8000/docs"
    
    # Wait for user to stop
    echo ""
    print_warning "Press Ctrl+C to stop the servers"
    wait
}

# Cleanup
cleanup() {
    print_status "Cleaning up..."
    
    # Remove deployment files
    rm -f backend-deployment.zip
    
    print_status "Cleanup completed!"
}

# Main deployment function
main() {
    case "${1:-help}" in
        "install")
            check_prerequisites
            install_dependencies
            ;;
        "deploy")
            check_prerequisites
            install_dependencies
            create_aws_resources
            deploy_backend
            deploy_frontend
            ;;
        "local")
            check_prerequisites
            install_dependencies
            start_local
            ;;
        "test")
            check_prerequisites
            install_dependencies
            run_tests
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|*)
            echo "Usage: $0 {install|deploy|local|test|cleanup|help}"
            echo ""
            echo "Commands:"
            echo "  install  - Install dependencies"
            echo "  deploy   - Deploy to AWS"
            echo "  local    - Start local development environment"
            echo "  test     - Run tests"
            echo "  cleanup  - Clean up deployment files"
            echo "  help     - Show this help message"
            ;;
    esac
}

# Run main function
main "$@" 
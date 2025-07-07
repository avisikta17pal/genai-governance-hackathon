#!/bin/bash

# EC2 User Data Script for GenAI Governance System
# This script runs when the EC2 instance starts up

# Update system
yum update -y

# Install Docker
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install

# Create application directory
mkdir -p /opt/genai-governance
cd /opt/genai-governance

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  genai-governance:
    image: genai-governance-system:latest
    build: .
    ports:
      - "8000:8000"
    environment:
      - AWS_DEFAULT_REGION=us-east-1
      - PYTHONPATH=/app
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - genai-governance
    restart: unless-stopped
EOF

# Create nginx configuration
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream genai_backend {
        server genai-governance:8000;
    }

    server {
        listen 80;
        server_name _;

        location / {
            proxy_pass http://genai_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://genai_backend/health;
            access_log off;
        }
    }
}
EOF

# Build and start the application
docker-compose up -d --build

# Create a simple monitoring script
cat > /opt/genai-governance/monitor.sh << 'EOF'
#!/bin/bash

# Simple monitoring script
while true; do
    if ! curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "$(date): Application health check failed, restarting..."
        docker-compose restart genai-governance
    fi
    sleep 60
done
EOF

chmod +x /opt/genai-governance/monitor.sh

# Start monitoring in background
nohup /opt/genai-governance/monitor.sh > /var/log/genai-monitor.log 2>&1 &

# Log completion
echo "GenAI Governance System deployment completed at $(date)" > /var/log/genai-deployment.log 
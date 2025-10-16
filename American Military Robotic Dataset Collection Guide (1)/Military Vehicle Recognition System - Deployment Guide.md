# Military Vehicle Recognition System - Deployment Guide

## Overview

This guide provides complete instructions for deploying the Autonomous Military Vehicle Recognition and Tactical AI System to production environments.

## System Architecture

The application consists of three main components:

1. **Frontend**: Professional web interface built with HTML5, CSS3, and JavaScript
2. **Backend API**: Flask REST API for model inference
3. **ML Model**: YOLOv8-Medium trained for military vehicle detection

## Deployment Options

### Option 1: AWS Deployment (Recommended)

#### Prerequisites
- AWS Account with EC2 and S3 access
- AWS CLI configured
- Docker installed (optional but recommended)

#### Step 1: Launch EC2 Instance
```bash
# Launch a GPU-enabled instance (recommended: g4dn.xlarge or p3.2xlarge)
# Or CPU instance (t3.large minimum) for cost savings

# Amazon Linux 2 or Ubuntu 22.04 LTS
# Open ports: 80, 443, 5000
```

#### Step 2: Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install system dependencies
sudo apt install libgl1-mesa-glx libglib2.0-0 -y
```

#### Step 3: Deploy Application
```bash
# Clone repository
git clone <your-repo-url>
cd military-vehicle-recognition-capstone/webapp/backend_api

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install Flask==3.1.1 flask-cors==6.0.0 Flask-SQLAlchemy==3.1.1
pip install Pillow==10.4.0
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install ultralytics opencv-python-headless

# Run application
python src/main.py
```

#### Step 4: Configure Nginx (Production)
```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/vehicle-recognition

# Add configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/vehicle-recognition /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 5: Setup Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/vehicle-recognition.service

# Add content:
[Unit]
Description=Military Vehicle Recognition API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/military-vehicle-recognition-capstone/webapp/backend_api
Environment="PATH=/home/ubuntu/military-vehicle-recognition-capstone/webapp/backend_api/venv/bin"
ExecStart=/home/ubuntu/military-vehicle-recognition-capstone/webapp/backend_api/venv/bin/python src/main.py

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable vehicle-recognition
sudo systemctl start vehicle-recognition
```

### Option 2: Google Cloud Platform (GCP)

#### Using Google Cloud Run
```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy application
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run application
CMD ["python", "src/main.py"]
EOF

# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/vehicle-recognition
gcloud run deploy vehicle-recognition \
    --image gcr.io/PROJECT_ID/vehicle-recognition \
    --platform managed \
    --region us-central1 \
    --memory 4Gi \
    --cpu 2
```

### Option 3: Azure App Service

```bash
# Create App Service
az webapp create \
    --resource-group myResourceGroup \
    --plan myAppServicePlan \
    --name vehicle-recognition \
    --runtime "PYTHON:3.11"

# Deploy code
az webapp deployment source config-zip \
    --resource-group myResourceGroup \
    --name vehicle-recognition \
    --src webapp.zip
```

### Option 4: Docker Deployment

```bash
# Build Docker image
docker build -t vehicle-recognition:latest .

# Run container
docker run -d \
    -p 5000:5000 \
    --name vehicle-recognition \
    vehicle-recognition:latest

# Or with GPU support
docker run -d \
    -p 5000:5000 \
    --gpus all \
    --name vehicle-recognition \
    vehicle-recognition:latest
```

### Option 5: Heroku

```bash
# Create Procfile
echo "web: python src/main.py" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy
heroku create vehicle-recognition-app
git push heroku main
```

## Environment Variables

Create a `.env` file:

```bash
FLASK_APP=src/main.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MODEL_PATH=../models/best.pt
CONFIDENCE_THRESHOLD=0.25
IOU_THRESHOLD=0.45
```

## Performance Optimization

### 1. Model Optimization
```python
# Export to ONNX for faster inference
from ultralytics import YOLO

model = YOLO('best.pt')
model.export(format='onnx')
```

### 2. Caching
```python
# Add Redis caching for frequent requests
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

### 3. Load Balancing
- Use AWS ELB, GCP Load Balancer, or Nginx for distributing traffic
- Deploy multiple instances behind load balancer

## Monitoring and Logging

### CloudWatch (AWS)
```bash
# Install CloudWatch agent
sudo apt install amazon-cloudwatch-agent

# Configure logging
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -s \
    -c file:/opt/aws/amazon-cloudwatch-agent/etc/config.json
```

### Application Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## Security Best Practices

1. **HTTPS**: Always use SSL/TLS certificates
2. **API Rate Limiting**: Implement rate limiting to prevent abuse
3. **Input Validation**: Validate all uploaded images
4. **CORS**: Configure CORS properly for production
5. **Secrets Management**: Use AWS Secrets Manager or similar

## Scaling Considerations

### Horizontal Scaling
- Deploy multiple instances
- Use container orchestration (Kubernetes, ECS)
- Implement auto-scaling based on CPU/memory usage

### Vertical Scaling
- Increase instance size for GPU workloads
- Use GPU instances for faster inference

## Cost Optimization

1. **Use CPU instances** for development/testing
2. **Spot instances** for non-critical workloads
3. **Auto-scaling** to match demand
4. **S3/Cloud Storage** for model weights instead of instance storage

## Troubleshooting

### Common Issues

**Issue**: Model not loading
```bash
# Check model path
ls -lh ../models/best.pt

# Verify permissions
chmod 644 ../models/best.pt
```

**Issue**: Out of memory
```bash
# Reduce batch size in detection.py
# Use model quantization
# Increase instance memory
```

**Issue**: Slow inference
```bash
# Use GPU instance
# Export model to ONNX/TensorRT
# Implement request queuing
```

## Health Checks

The application provides health check endpoints:

```bash
# Check API health
curl http://your-domain.com/api/health

# Expected response:
{
    "status": "healthy",
    "model_loaded": true,
    "model_path": "/path/to/best.pt",
    "yolo_available": true
}
```

## Backup and Recovery

```bash
# Backup model weights
aws s3 cp ../models/best.pt s3://your-bucket/models/best.pt

# Backup database
sqlite3 src/database/app.db .dump > backup.sql

# Restore
sqlite3 src/database/app.db < backup.sql
```

## Support

For deployment issues or questions:
- Check logs: `tail -f app.log`
- Review system resources: `htop` or `nvidia-smi`
- Test API endpoints manually with curl or Postman

## License

This project is licensed under the MIT License - see LICENSE file for details.


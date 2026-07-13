#!/usr/bin/env bash

# ==============================================================================
# AWS EC2 Docker Deployment Script - AI Contract Intelligence
# ==============================================================================
# This script automates:
#   1. Authenticating with AWS ECR (Elastic Container Registry)
#   2. Building the lightweight production Docker image
#   3. Tagging and pushing the image to ECR
#   4. Deploying and running the container on the target EC2 instance
#
# Prerequisites:
#   - AWS CLI configured on local machine (with permissions to ECR/EC2)
#   - Docker running locally
#   - Target EC2 instance with Docker installed and security groups allowing Port 8000
# ==============================================================================

# Exit immediately if any command fails
set -e

# --- CONFIGURATION (Adjust for your environment) ---
AWS_REGION="us-east-1"
AWS_ACCOUNT_ID="123456789012" # Replace with your AWS Account ID
ECR_REPO_NAME="contract-intelligence-backend"
IMAGE_TAG="latest"
EC2_PUBLIC_DNS="ec2-3-80-120-45.compute-1.amazonaws.com" # Replace with EC2 DNS or IP
EC2_SSH_KEY="~/.ssh/my-contract-app-key.pem" # Path to your SSH private key (.pem)
EC2_USER="ubuntu" # 'ubuntu' for Ubuntu AMI, 'ecr-user' or 'admin' for others

# Full ECR registry URL
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
FULL_IMAGE_URI="${ECR_REGISTRY}/${ECR_REPO_NAME}:${IMAGE_TAG}"

echo "======================================================================"
echo "🚀 Starting Deployment Pipeline for: ${ECR_REPO_NAME}"
echo "======================================================================"

# 1. Authenticate Docker with AWS ECR
echo "🔑 Logging in to AWS ECR..."
aws ecr get-login-password --region "${AWS_REGION}" | \
    docker login --username AWS --password-stdin "${ECR_REGISTRY}"

# 2. Build the Docker Image
echo "📦 Building production Docker image..."
# Using --pull ensures we get the latest slim parent image
docker build --pull -t "${ECR_REPO_NAME}" .

# 3. Tag and Push the Image to AWS ECR
echo "🏷️ Tagging image..."
docker tag "${ECR_REPO_NAME}:${IMAGE_TAG}" "${FULL_IMAGE_URI}"

echo "📤 Pushing image to AWS ECR registry..."
docker push "${FULL_IMAGE_URI}"

echo "✅ Image successfully pushed: ${FULL_IMAGE_URI}"

# 4. Deploy to AWS EC2 Instance via SSH
echo "🖥️ Deploying to EC2 Instance [${EC2_PUBLIC_DNS}]..."

# We verify that PINECONE_API_KEY is set locally so it can be forwarded to EC2
if [ -z "${PINECONE_API_KEY}" ]; then
    echo "⚠️ WARNING: PINECONE_API_KEY environment variable is not set locally."
    echo "Please input your PINECONE_API_KEY now to securely inject it into the EC2 environment:"
    read -rsp "Pinecone API Key: " PINECONE_API_KEY
    echo ""
fi

if [ -z "${PINECONE_INDEX}" ]; then
    echo "Using default PINECONE_INDEX..."
    PINECONE_INDEX="contract-index"
fi

# SSH commands to execute on the EC2 instance
# - Authenticates Docker on the EC2 host with ECR
# - Pulls the latest container image
# - Stops and removes any existing container of the same name
# - Runs the new container, passing PINECONE_API_KEY as an env variable securely
SSH_COMMANDS=$(cat <<EOF
    # Authenticate local Docker daemon with AWS ECR
    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}

    # Pull the latest container version
    docker pull ${FULL_IMAGE_URI}

    # Stop current running instance if it exists
    docker stop ${ECR_REPO_NAME} || true
    docker rm ${ECR_REPO_NAME} || true

    # Run the container with injected system environment variables
    # Port 8000 on the host is bound to 8000 inside the container
    docker run -d \
      --name ${ECR_REPO_NAME} \
      -p 8000:8000 \
      -e PINECONE_API_KEY="${PINECONE_API_KEY}" \
      -e PINECONE_INDEX="${PINECONE_INDEX}" \
      --restart unless-stopped \
      ${FULL_IMAGE_URI}

    # Clean up dangling images to save EC2 disk space
    docker image prune -f
EOF
)

# Execute the deployment commands on EC2 via SSH
ssh -i "${EC2_SSH_KEY}" -o StrictHostKeyChecking=no "${EC2_USER}@${EC2_PUBLIC_DNS}" "${SSH_COMMANDS}"

echo "======================================================================"
echo "🎉 Deployment Completed Successfully!"
echo "Your API is running at: http://${EC2_PUBLIC_DNS}:8000/"
echo "======================================================================"

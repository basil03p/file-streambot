#!/bin/bash
# Azure Deployment Script for FileStreamBot
# This script automates the deployment process to Azure

set -e

echo "🚀 Azure FileStreamBot Deployment Script"
echo "========================================="

# Configuration
RESOURCE_GROUP="filestream-rg"
LOCATION="eastus"
CONTAINER_NAME="filestream-bot"
DNS_LABEL="filestream-$(date +%s)"
IMAGE_NAME="your-dockerhub-username/filestream-bot:latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if Azure CLI is installed
    if ! command -v az &> /dev/null; then
        print_error "Azure CLI is not installed. Please install it first."
        echo "Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
        exit 1
    fi
    
    # Check if logged in to Azure
    if ! az account show &> /dev/null; then
        print_warning "Not logged in to Azure. Please login."
        az login
    fi
    
    print_success "Prerequisites check completed!"
}

create_resource_group() {
    print_status "Creating resource group: $RESOURCE_GROUP"
    
    if az group show --name $RESOURCE_GROUP &> /dev/null; then
        print_warning "Resource group $RESOURCE_GROUP already exists."
    else
        az group create --name $RESOURCE_GROUP --location $LOCATION
        print_success "Resource group created!"
    fi
}

get_environment_variables() {
    print_status "Setting up environment variables..."
    
    # Check if .env file exists
    if [ -f ".env" ]; then
        print_success "Found .env file, reading configuration..."
        source .env
    else
        print_warning ".env file not found. Please provide configuration manually."
        
        read -p "Enter your API_ID: " API_ID
        read -p "Enter your API_HASH: " API_HASH
        read -p "Enter your BOT_TOKEN: " BOT_TOKEN
        read -p "Enter your OWNER_ID: " OWNER_ID
        read -p "Enter your DATABASE_URL: " DATABASE_URL
        
        # Optional multi-bot tokens
        read -p "Enter MULTITOKEN1 (or press Enter to skip): " MULTITOKEN1
        read -p "Enter MULTITOKEN2 (or press Enter to skip): " MULTITOKEN2
        read -p "Enter MULTITOKEN3 (or press Enter to skip): " MULTITOKEN3
    fi
    
    # Validate required variables
    if [ -z "$API_ID" ] || [ -z "$API_HASH" ] || [ -z "$BOT_TOKEN" ] || [ -z "$OWNER_ID" ] || [ -z "$DATABASE_URL" ]; then
        print_error "Missing required environment variables!"
        exit 1
    fi
    
    print_success "Environment variables configured!"
}

deploy_container() {
    print_status "Deploying container to Azure Container Instances..."
    
    # Build environment variables string
    ENV_VARS="API_ID=$API_ID API_HASH=$API_HASH BOT_TOKEN=$BOT_TOKEN OWNER_ID=$OWNER_ID DATABASE_URL=$DATABASE_URL PORT=8080 BIND_ADDRESS=0.0.0.0 HAS_SSL=true NO_PORT=true"
    
    # Add multi-bot tokens if available
    if [ ! -z "$MULTITOKEN1" ]; then
        ENV_VARS="$ENV_VARS MULTI_BOT_MODE=true MULTITOKEN1=$MULTITOKEN1"
    fi
    if [ ! -z "$MULTITOKEN2" ]; then
        ENV_VARS="$ENV_VARS MULTITOKEN2=$MULTITOKEN2"
    fi
    if [ ! -z "$MULTITOKEN3" ]; then
        ENV_VARS="$ENV_VARS MULTITOKEN3=$MULTITOKEN3"
    fi
    
    # Add channel configuration if available
    if [ ! -z "$AUTH_CHANNEL" ]; then
        ENV_VARS="$ENV_VARS AUTH_CHANNEL=$AUTH_CHANNEL GENERATE_DOWNLOAD_LINKS=true"
    fi
    if [ ! -z "$FLOG_CHANNEL" ]; then
        ENV_VARS="$ENV_VARS FLOG_CHANNEL=$FLOG_CHANNEL"
    fi
    if [ ! -z "$ULOG_CHANNEL" ]; then
        ENV_VARS="$ENV_VARS ULOG_CHANNEL=$ULOG_CHANNEL"
    fi
    
    # Deploy container
    az container create \
        --name $CONTAINER_NAME \
        --resource-group $RESOURCE_GROUP \
        --image $IMAGE_NAME \
        --location $LOCATION \
        --cpu 1 \
        --memory 2 \
        --ports 8080 \
        --dns-name-label $DNS_LABEL \
        --restart-policy Always \
        --environment-variables $ENV_VARS
    
    print_success "Container deployed successfully!"
}

get_deployment_info() {
    print_status "Getting deployment information..."
    
    # Get FQDN
    FQDN=$(az container show --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP --query "ipAddress.fqdn" --output tsv)
    
    # Get public IP
    PUBLIC_IP=$(az container show --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP --query "ipAddress.ip" --output tsv)
    
    echo ""
    echo "🎉 Deployment completed successfully!"
    echo "====================================="
    echo "Container Name: $CONTAINER_NAME"
    echo "Resource Group: $RESOURCE_GROUP"
    echo "Location: $LOCATION"
    echo "FQDN: https://$FQDN"
    echo "Public IP: $PUBLIC_IP"
    echo "Bot URL: https://$FQDN"
    echo ""
    
    # Update FQDN in environment if needed
    if [ -f ".env" ]; then
        if grep -q "FQDN=" .env; then
            sed -i "s/FQDN=.*/FQDN=$FQDN/" .env
        else
            echo "FQDN=$FQDN" >> .env
        fi
        print_success "Updated FQDN in .env file"
    fi
}

check_deployment() {
    print_status "Checking deployment status..."
    
    # Wait for container to be running
    echo "Waiting for container to start..."
    sleep 30
    
    # Get container state
    STATE=$(az container show --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP --query "containers[0].instanceView.currentState.state" --output tsv)
    
    if [ "$STATE" = "Running" ]; then
        print_success "Container is running!"
        
        # Try to access the health endpoint
        FQDN=$(az container show --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP --query "ipAddress.fqdn" --output tsv)
        
        echo "Testing bot accessibility..."
        if curl -f "https://$FQDN/health" &> /dev/null; then
            print_success "Bot is accessible and healthy!"
        else
            print_warning "Bot may still be starting up. Check logs if issues persist."
        fi
    else
        print_warning "Container state: $STATE"
        print_status "Checking logs..."
        az container logs --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP
    fi
}

show_management_commands() {
    echo ""
    echo "📋 Management Commands"
    echo "====================="
    echo "View logs:           az container logs --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP"
    echo "Restart container:   az container restart --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP"
    echo "Stop container:      az container stop --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP"
    echo "Delete container:    az container delete --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP --yes"
    echo "Delete resource group: az group delete --name $RESOURCE_GROUP --yes"
    echo ""
}

# Main execution
main() {
    print_status "Starting Azure deployment process..."
    
    check_prerequisites
    create_resource_group
    get_environment_variables
    deploy_container
    get_deployment_info
    check_deployment
    show_management_commands
    
    print_success "Azure deployment completed! Your FileStreamBot is now running on Azure! 🚀"
}

# Check if script is being run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

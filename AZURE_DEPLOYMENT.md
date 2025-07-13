# 🌐 Azure Deployment Guide for FileStreamBot

Complete guide to deploy FileStreamBot on Microsoft Azure with multiple hosting options.

## 🚀 Azure Hosting Options

### 1. **Azure Container Instances (ACI)** - Recommended for beginners
- Simple container deployment
- Pay-per-second billing
- No server management
- Perfect for small to medium bots

### 2. **Azure Container Apps** - Recommended for production
- Serverless container platform
- Auto-scaling
- Built-in load balancing
- Perfect for high-traffic bots

### 3. **Azure App Service** - Traditional web app hosting
- Platform-as-a-Service (PaaS)
- Built-in CI/CD
- Easy scaling
- Great for web applications

### 4. **Azure Kubernetes Service (AKS)** - For advanced users
- Full Kubernetes cluster
- Maximum control and scaling
- Enterprise-grade features

## 🎯 **Option 1: Azure Container Instances (Quick Start)**

### Prerequisites
- Azure account with active subscription
- Docker installed locally
- Azure CLI installed

### Step 1: Install Azure CLI
```bash
# Windows
winget install Microsoft.AzureCLI

# macOS
brew install azure-cli

# Linux
curl -sL https://aka.ms/InstallAzureCLI | sudo bash
```

### Step 2: Login to Azure
```bash
az login
```

### Step 3: Create Resource Group
```bash
# Create resource group
az group create --name filestream-rg --location eastus

# Set default resource group
az configure --defaults group=filestream-rg
```

### Step 4: Create Container Registry (Optional)
```bash
# Create Azure Container Registry
az acr create --name filestreamregistry --sku Basic

# Login to registry
az acr login --name filestreamregistry
```

### Step 5: Deploy Container Instance
```bash
# Deploy directly from Docker Hub (if image is public)
az container create \
  --name filestream-bot \
  --image your-dockerhub-username/filestream-bot:latest \
  --resource-group filestream-rg \
  --location eastus \
  --cpu 1 \
  --memory 2 \
  --ports 8080 \
  --dns-name-label filestream-unique-name \
  --environment-variables \
    API_ID=your_api_id \
    API_HASH=your_api_hash \
    BOT_TOKEN=your_bot_token \
    OWNER_ID=your_owner_id \
    DATABASE_URL=your_mongodb_url \
    MULTI_BOT_MODE=true \
    MULTITOKEN1=your_helper_token_1 \
    MULTITOKEN2=your_helper_token_2 \
    MULTITOKEN3=your_helper_token_3 \
    PORT=8080 \
    FQDN=filestream-unique-name.eastus.azurecontainer.io \
    HAS_SSL=true \
    NO_PORT=true
```

### Step 6: Check Deployment
```bash
# Check container status
az container show --name filestream-bot --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}"

# Get logs
az container logs --name filestream-bot
```

## 🔥 **Option 2: Azure Container Apps (Production)**

### Step 1: Install Container Apps Extension
```bash
az extension add --name containerapp
```

### Step 2: Create Container Apps Environment
```bash
# Create environment
az containerapp env create \
  --name filestream-env \
  --resource-group filestream-rg \
  --location eastus
```

### Step 3: Deploy Container App
```bash
az containerapp create \
  --name filestream-bot \
  --resource-group filestream-rg \
  --environment filestream-env \
  --image your-dockerhub-username/filestream-bot:latest \
  --target-port 8080 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 3 \
  --cpu 1.0 \
  --memory 2.0Gi \
  --env-vars \
    API_ID=your_api_id \
    API_HASH=your_api_hash \
    BOT_TOKEN=your_bot_token \
    OWNER_ID=your_owner_id \
    DATABASE_URL=your_mongodb_url \
    MULTI_BOT_MODE=true \
    MULTITOKEN1=your_helper_token_1 \
    MULTITOKEN2=your_helper_token_2 \
    MULTITOKEN3=your_helper_token_3 \
    PORT=8080 \
    HAS_SSL=true \
    NO_PORT=true
```

### Step 4: Get Application URL
```bash
az containerapp show --name filestream-bot --query properties.configuration.ingress.fqdn
```

## 🌐 **Option 3: Azure App Service**

### Step 1: Create App Service Plan
```bash
az appservice plan create \
  --name filestream-plan \
  --resource-group filestream-rg \
  --location eastus \
  --sku B1 \
  --is-linux
```

### Step 2: Create Web App
```bash
az webapp create \
  --name filestream-webapp \
  --resource-group filestream-rg \
  --plan filestream-plan \
  --deployment-container-image-name your-dockerhub-username/filestream-bot:latest
```

### Step 3: Configure Environment Variables
```bash
az webapp config appsettings set \
  --name filestream-webapp \
  --resource-group filestream-rg \
  --settings \
    API_ID=your_api_id \
    API_HASH=your_api_hash \
    BOT_TOKEN=your_bot_token \
    OWNER_ID=your_owner_id \
    DATABASE_URL=your_mongodb_url \
    MULTI_BOT_MODE=true \
    MULTITOKEN1=your_helper_token_1 \
    MULTITOKEN2=your_helper_token_2 \
    MULTITOKEN3=your_helper_token_3 \
    PORT=8080 \
    WEBSITES_PORT=8080 \
    HAS_SSL=true \
    NO_PORT=true
```

## 💾 **Database Options for Azure**

### Option 1: Azure Cosmos DB (MongoDB API)
```bash
# Create Cosmos DB account
az cosmosdb create \
  --name filestream-cosmos \
  --resource-group filestream-rg \
  --kind MongoDB \
  --server-version 4.2

# Get connection string
az cosmosdb keys list --name filestream-cosmos --type connection-strings
```

### Option 2: MongoDB Atlas (Recommended)
- Use your existing MongoDB Atlas connection
- No additional Azure configuration needed
- Better performance and reliability

### Option 3: Azure Database for MongoDB
```bash
# Alternative managed MongoDB service
az mongodb flexible-server create \
  --name filestream-mongodb \
  --resource-group filestream-rg \
  --location eastus \
  --admin-user dbadmin \
  --admin-password YourStrongPassword123!
```

## 🔐 **Secure Configuration with Azure Key Vault**

### Step 1: Create Key Vault
```bash
az keyvault create \
  --name filestream-keyvault \
  --resource-group filestream-rg \
  --location eastus
```

### Step 2: Store Secrets
```bash
# Store sensitive configuration
az keyvault secret set --vault-name filestream-keyvault --name "api-id" --value "your_api_id"
az keyvault secret set --vault-name filestream-keyvault --name "api-hash" --value "your_api_hash"
az keyvault secret set --vault-name filestream-keyvault --name "bot-token" --value "your_bot_token"
az keyvault secret set --vault-name filestream-keyvault --name "database-url" --value "your_mongodb_url"
az keyvault secret set --vault-name filestream-keyvault --name "multitoken1" --value "your_helper_token_1"
```

### Step 3: Configure App to Use Key Vault
```bash
# For Container Apps
az containerapp update \
  --name filestream-bot \
  --set-env-vars \
    API_ID=secretref:api-id \
    API_HASH=secretref:api-hash \
    BOT_TOKEN=secretref:bot-token
```

## 🏗️ **Azure DevOps CI/CD Pipeline**

### azure-pipelines.yml
```yaml
trigger:
- main

variables:
  dockerRegistryServiceConnection: 'your-docker-connection'
  imageRepository: 'filestream-bot'
  containerRegistry: 'filestreamregistry.azurecr.io'
  dockerfilePath: '$(Build.SourcesDirectory)/Dockerfile'
  tag: '$(Build.BuildId)'

stages:
- stage: Build
  displayName: Build and push stage
  jobs:
  - job: Build
    displayName: Build
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: Docker@2
      displayName: Build and push an image to container registry
      inputs:
        command: buildAndPush
        repository: $(imageRepository)
        dockerfile: $(dockerfilePath)
        containerRegistry: $(dockerRegistryServiceConnection)
        tags: |
          $(tag)
          latest

- stage: Deploy
  displayName: Deploy stage
  dependsOn: Build
  jobs:
  - deployment: Deploy
    displayName: Deploy
    pool:
      vmImage: 'ubuntu-latest'
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureContainerInstances@0
            displayName: 'Deploy to Azure Container Instances'
            inputs:
              azureSubscription: 'your-azure-subscription'
              resourceGroupName: 'filestream-rg'
              location: 'eastus'
              containerName: 'filestream-bot'
              imageName: '$(containerRegistry)/$(imageRepository):$(tag)'
```

## 📊 **Monitoring and Logging**

### Enable Application Insights
```bash
# Create Application Insights
az monitor app-insights component create \
  --app filestream-insights \
  --location eastus \
  --resource-group filestream-rg

# Get instrumentation key
az monitor app-insights component show \
  --app filestream-insights \
  --resource-group filestream-rg \
  --query instrumentationKey
```

### Configure Log Analytics
```bash
# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --workspace-name filestream-logs \
  --resource-group filestream-rg \
  --location eastus
```

## 💰 **Cost Optimization**

### Container Instances Pricing
- **CPU**: ~$0.0012 per vCPU per hour
- **Memory**: ~$0.000175 per GB per hour
- **Example**: 1 vCPU + 2GB RAM = ~$1.15/day

### Container Apps Pricing
- **Consumption**: Pay only for active usage
- **Dedicated**: Fixed pricing for guaranteed resources
- **Free tier**: 180,000 vCPU seconds/month

### Cost-Saving Tips
1. **Use consumption pricing** for variable workloads
2. **Scale to zero** during idle periods
3. **Monitor resource usage** with Azure Monitor
4. **Use Azure Calculator** for cost estimation

## 🛠️ **Troubleshooting**

### Common Issues

#### Container Won't Start
```bash
# Check container logs
az container logs --name filestream-bot

# Check container status
az container show --name filestream-bot
```

#### Environment Variables Not Loading
```bash
# Verify environment variables
az container show --name filestream-bot --query containers[0].environmentVariables

# Update environment variables
az container restart --name filestream-bot
```

#### Port Issues
```bash
# Ensure PORT environment variable matches container port
# Default: PORT=8080
# Make sure Dockerfile exposes the same port
```

### Performance Optimization
1. **Increase CPU/Memory** if bot is slow
2. **Use Premium storage** for better I/O
3. **Enable caching** with Azure Redis
4. **Use CDN** for file serving

## 🎯 **Best Practices**

### Security
1. **Use Key Vault** for sensitive data
2. **Enable HTTPS** with custom domain
3. **Restrict network access** with NSGs
4. **Regular security updates**

### Monitoring
1. **Set up alerts** for critical metrics
2. **Monitor costs** regularly
3. **Use Log Analytics** for debugging
4. **Track performance** metrics

### Scaling
1. **Start small** and scale as needed
2. **Use auto-scaling** for variable loads
3. **Monitor resource utilization**
4. **Plan for peak usage**

## 🎉 **Quick Start Commands**

### Deploy to Azure Container Instances (Fastest)
```bash
# Login and create resource group
az login
az group create --name filestream-rg --location eastus

# Deploy container
az container create \
  --name filestream-bot \
  --image your-dockerhub-username/filestream-bot:latest \
  --resource-group filestream-rg \
  --cpu 1 --memory 2 --ports 8080 \
  --dns-name-label filestream-$(date +%s) \
  --environment-variables \
    API_ID=your_api_id \
    BOT_TOKEN=your_bot_token \
    DATABASE_URL=your_mongodb_url \
    PORT=8080

# Get URL
az container show --name filestream-bot --query ipAddress.fqdn
```

---

## 📚 **Next Steps**

1. **Choose your preferred Azure option**
2. **Prepare your Docker image**
3. **Configure environment variables**
4. **Deploy and test**
5. **Set up monitoring**
6. **Configure custom domain** (optional)

**Your FileStreamBot will be running on Azure with enterprise-grade reliability!** 🚀

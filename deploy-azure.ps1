# Azure Deployment Script for FileStreamBot (PowerShell)
# This script automates the deployment process to Azure for Windows users

param(
    [string]$ResourceGroup = "filestream-rg",
    [string]$Location = "eastus",
    [string]$ContainerName = "filestream-bot",
    [string]$ImageName = "your-dockerhub-username/filestream-bot:latest"
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Cyan"

function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

function Test-Prerequisites {
    Write-Status "Checking prerequisites..."
    
    # Check if Azure CLI is installed
    try {
        $azVersion = az version --output json | ConvertFrom-Json
        Write-Success "Azure CLI version $($azVersion.'azure-cli') detected"
    }
    catch {
        Write-Error "Azure CLI is not installed. Please install it first."
        Write-Host "Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
        exit 1
    }
    
    # Check if logged in to Azure
    try {
        $account = az account show --output json | ConvertFrom-Json
        Write-Success "Logged in as: $($account.user.name)"
    }
    catch {
        Write-Warning "Not logged in to Azure. Please login."
        az login
    }
    
    Write-Success "Prerequisites check completed!"
}

function New-ResourceGroup {
    Write-Status "Creating resource group: $ResourceGroup"
    
    try {
        $existingRg = az group show --name $ResourceGroup --output json 2>$null | ConvertFrom-Json
        Write-Warning "Resource group $ResourceGroup already exists."
    }
    catch {
        az group create --name $ResourceGroup --location $Location --output json | Out-Null
        Write-Success "Resource group created!"
    }
}

function Get-EnvironmentVariables {
    Write-Status "Setting up environment variables..."
    
    # Check if .env file exists
    if (Test-Path ".env") {
        Write-Success "Found .env file, reading configuration..."
        
        # Read .env file
        $envVars = @{}
        Get-Content ".env" | ForEach-Object {
            if ($_ -match "^([^=]+)=(.*)$") {
                $envVars[$matches[1]] = $matches[2]
            }
        }
        
        # Set variables
        $script:API_ID = $envVars["API_ID"]
        $script:API_HASH = $envVars["API_HASH"]
        $script:BOT_TOKEN = $envVars["BOT_TOKEN"]
        $script:OWNER_ID = $envVars["OWNER_ID"]
        $script:DATABASE_URL = $envVars["DATABASE_URL"]
        $script:MULTI_BOT_MODE = $envVars["MULTI_BOT_MODE"]
        $script:MULTITOKEN1 = $envVars["MULTITOKEN1"]
        $script:MULTITOKEN2 = $envVars["MULTITOKEN2"]
        $script:MULTITOKEN3 = $envVars["MULTITOKEN3"]
        $script:MULTITOKEN4 = $envVars["MULTITOKEN4"]
        $script:MULTITOKEN5 = $envVars["MULTITOKEN5"]
        $script:MULTITOKEN6 = $envVars["MULTITOKEN6"]
        $script:MULTITOKEN7 = $envVars["MULTITOKEN7"]
        $script:AUTH_CHANNEL = $envVars["AUTH_CHANNEL"]
        $script:FLOG_CHANNEL = $envVars["FLOG_CHANNEL"]
        $script:ULOG_CHANNEL = $envVars["ULOG_CHANNEL"]
        $script:FORCE_SUB_ID = $envVars["FORCE_SUB_ID"]
    }
    else {
        Write-Warning ".env file not found. Please provide configuration manually."
        
        $script:API_ID = Read-Host "Enter your API_ID"
        $script:API_HASH = Read-Host "Enter your API_HASH"
        $script:BOT_TOKEN = Read-Host "Enter your BOT_TOKEN"
        $script:OWNER_ID = Read-Host "Enter your OWNER_ID"
        $script:DATABASE_URL = Read-Host "Enter your DATABASE_URL"
        
        # Optional multi-bot tokens
        $script:MULTITOKEN1 = Read-Host "Enter MULTITOKEN1 (or press Enter to skip)"
        $script:MULTITOKEN2 = Read-Host "Enter MULTITOKEN2 (or press Enter to skip)"
        $script:MULTITOKEN3 = Read-Host "Enter MULTITOKEN3 (or press Enter to skip)"
    }
    
    # Validate required variables
    if (-not $API_ID -or -not $API_HASH -or -not $BOT_TOKEN -or -not $OWNER_ID -or -not $DATABASE_URL) {
        Write-Error "Missing required environment variables!"
        exit 1
    }
    
    Write-Success "Environment variables configured!"
}

function Deploy-Container {
    Write-Status "Deploying container to Azure Container Instances..."
    
    # Generate unique DNS label
    $dnsLabel = "filestream-$(Get-Date -Format 'yyyyMMddHHmmss')"
    
    # Build environment variables array
    $envVars = @(
        "API_ID=$API_ID",
        "API_HASH=$API_HASH",
        "BOT_TOKEN=$BOT_TOKEN",
        "OWNER_ID=$OWNER_ID",
        "DATABASE_URL=$DATABASE_URL",
        "PORT=8080",
        "BIND_ADDRESS=0.0.0.0",
        "HAS_SSL=true",
        "NO_PORT=true",
        "FQDN=$dnsLabel.eastus.azurecontainer.io"
    )
    
    # Add multi-bot tokens if available
    if ($MULTITOKEN1) {
        $envVars += "MULTI_BOT_MODE=true"
        $envVars += "MULTITOKEN1=$MULTITOKEN1"
    }
    if ($MULTITOKEN2) { $envVars += "MULTITOKEN2=$MULTITOKEN2" }
    if ($MULTITOKEN3) { $envVars += "MULTITOKEN3=$MULTITOKEN3" }
    if ($MULTITOKEN4) { $envVars += "MULTITOKEN4=$MULTITOKEN4" }
    if ($MULTITOKEN5) { $envVars += "MULTITOKEN5=$MULTITOKEN5" }
    if ($MULTITOKEN6) { $envVars += "MULTITOKEN6=$MULTITOKEN6" }
    if ($MULTITOKEN7) { $envVars += "MULTITOKEN7=$MULTITOKEN7" }
    
    # Add channel configuration if available
    if ($AUTH_CHANNEL) {
        $envVars += "AUTH_CHANNEL=$AUTH_CHANNEL"
        $envVars += "GENERATE_DOWNLOAD_LINKS=true"
    }
    if ($FLOG_CHANNEL) { $envVars += "FLOG_CHANNEL=$FLOG_CHANNEL" }
    if ($ULOG_CHANNEL) { $envVars += "ULOG_CHANNEL=$ULOG_CHANNEL" }
    if ($FORCE_SUB_ID) {
        $envVars += "FORCE_SUB_ID=$FORCE_SUB_ID"
        $envVars += "FORCE_SUB=true"
    }
    
    # Deploy container
    $deploymentArgs = @(
        "container", "create",
        "--name", $ContainerName,
        "--resource-group", $ResourceGroup,
        "--image", $ImageName,
        "--location", $Location,
        "--cpu", "1",
        "--memory", "2",
        "--ports", "8080",
        "--dns-name-label", $dnsLabel,
        "--restart-policy", "Always",
        "--environment-variables"
    ) + $envVars
    
    & az @deploymentArgs | Out-Null
    
    Write-Success "Container deployed successfully!"
    return $dnsLabel
}

function Get-DeploymentInfo {
    param([string]$DnsLabel)
    
    Write-Status "Getting deployment information..."
    
    # Get FQDN
    $fqdn = az container show --name $ContainerName --resource-group $ResourceGroup --query "ipAddress.fqdn" --output tsv
    
    # Get public IP
    $publicIp = az container show --name $ContainerName --resource-group $ResourceGroup --query "ipAddress.ip" --output tsv
    
    Write-Host ""
    Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host "Container Name: $ContainerName"
    Write-Host "Resource Group: $ResourceGroup"
    Write-Host "Location: $Location"
    Write-Host "FQDN: https://$fqdn"
    Write-Host "Public IP: $publicIp"
    Write-Host "Bot URL: https://$fqdn"
    Write-Host ""
    
    # Update FQDN in environment if needed
    if (Test-Path ".env") {
        $envContent = Get-Content ".env"
        $fqdnLineExists = $false
        
        for ($i = 0; $i -lt $envContent.Length; $i++) {
            if ($envContent[$i] -match "^FQDN=") {
                $envContent[$i] = "FQDN=$fqdn"
                $fqdnLineExists = $true
                break
            }
        }
        
        if (-not $fqdnLineExists) {
            $envContent += "FQDN=$fqdn"
        }
        
        $envContent | Set-Content ".env"
        Write-Success "Updated FQDN in .env file"
    }
    
    return $fqdn
}

function Test-Deployment {
    param([string]$Fqdn)
    
    Write-Status "Checking deployment status..."
    
    # Wait for container to start
    Write-Host "Waiting for container to start..."
    Start-Sleep -Seconds 30
    
    # Get container state
    $state = az container show --name $ContainerName --resource-group $ResourceGroup --query "containers[0].instanceView.currentState.state" --output tsv
    
    if ($state -eq "Running") {
        Write-Success "Container is running!"
        
        # Try to access the health endpoint
        Write-Host "Testing bot accessibility..."
        try {
            $response = Invoke-WebRequest -Uri "https://$Fqdn/health" -TimeoutSec 10
            Write-Success "Bot is accessible and healthy!"
        }
        catch {
            Write-Warning "Bot may still be starting up. Check logs if issues persist."
        }
    }
    else {
        Write-Warning "Container state: $state"
        Write-Status "Checking logs..."
        az container logs --name $ContainerName --resource-group $ResourceGroup
    }
}

function Show-ManagementCommands {
    Write-Host ""
    Write-Host "📋 Management Commands" -ForegroundColor Cyan
    Write-Host "=====================" -ForegroundColor Cyan
    Write-Host "View logs:           az container logs --name $ContainerName --resource-group $ResourceGroup"
    Write-Host "Restart container:   az container restart --name $ContainerName --resource-group $ResourceGroup"
    Write-Host "Stop container:      az container stop --name $ContainerName --resource-group $ResourceGroup"
    Write-Host "Delete container:    az container delete --name $ContainerName --resource-group $ResourceGroup --yes"
    Write-Host "Delete resource group: az group delete --name $ResourceGroup --yes"
    Write-Host ""
}

# Main execution
function Main {
    Write-Host "🚀 Azure FileStreamBot Deployment Script" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    
    Test-Prerequisites
    New-ResourceGroup
    Get-EnvironmentVariables
    $dnsLabel = Deploy-Container
    $fqdn = Get-DeploymentInfo -DnsLabel $dnsLabel
    Test-Deployment -Fqdn $fqdn
    Show-ManagementCommands
    
    Write-Success "Azure deployment completed! Your FileStreamBot is now running on Azure! 🚀"
}

# Execute main function
Main

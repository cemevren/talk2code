#!/bin/bash

NAMESPACE="talk2code"


helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add qdrant https://qdrant.github.io/qdrant-helm
helm repo update

# Ensure Minikube is running
# Check if minikube is running
minikube_status=$(minikube status --format='{{.Host}}')

if [ "$minikube_status" != "Running" ]; then
    echo "Minikube is not running. Starting minikube..."
    minikube start --driver=docker
else
    echo "Minikube is already running."
fi

minikube addons enable metrics-server
minikube addons enable ingress

# Create namespace if it doesn't exist
kubectl get namespace $NAMESPACE || kubectl create namespace $NAMESPACE

# Install PostgreSQL
echo "Installing PostgreSQL"
helm upgrade -i postgres bitnami/postgresql -f ./helm-charts/postgres/values.yaml --namespace $NAMESPACE 
echo "PostgreSQL has been installed"

# Build the backend
echo "Building Fast API Backend"
eval $(minikube docker-env)
docker build -t talk2code-backend:latest ./backend/
eval $(minikube docker-env -u)
echo "Installing Fast API Backend"
helm upgrade --install talk2code-backend ./helm-charts/backend --namespace $NAMESPACE 


echo "Installing Qdrant"
helm upgrade -i qdrant qdrant/qdrant --namespace $NAMESPACE 
echo "Qdrant has been installed"

# Starting the dashboard
minikube dashboard
# You can add additional Helm install commands for other charts here
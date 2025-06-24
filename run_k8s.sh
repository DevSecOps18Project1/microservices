#!/bin/bash

# Postgres Database
kubectl apply -f database/k8s/k8s-secret.yaml
kubectl apply -f database/k8s/k8s-db-configmap.yaml
kubectl apply -f database/k8s/k8s-pvc.yaml
kubectl apply -f database/k8s/k8s-postgres-deployment.yaml
kubectl apply -f database/k8s/k8s-postgres-service.yaml

# Flask application
kubectl apply -f backend/k8s/k8s-app-configmap.yaml
kubectl apply -f backend/k8s/k8s-flask-deployment.yaml
kubectl apply -f backend/k8s/k8s-flask-service.yaml

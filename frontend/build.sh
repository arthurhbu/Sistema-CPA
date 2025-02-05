#!/bin/bash
version="v$(date +'%Y%m%d')"
# Limpa os repositórios locais
podman rmi sistema-frontend:$version
podman rmi sistema-frontend:latest
podman build . -t sistema-frontend:$version -t sistema-frontend:latest

# Faz o login para enviar aos repositórios públicos
podman login quay.io --authfile ../auth.json

podman push sistema-frontend:$version quay.io/uemcpa/sistema-frontend:$version --authfile ../auth.json
podman push sistema-frontend:latest quay.io/uemcpa/sistema-frontend:latest --authfile ../auth.json
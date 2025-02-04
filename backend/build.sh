#!/bin/bash
version="v$(date +'%Y%m%d')"
# Limpa os repositórios locais
podman rmi sistema-backend:$version
podman rmi sistema-backend:latest
podman build . -t sistema-backend:$version -t sistema-backend:latest

# Faz o login para enviar aos repositórios públicos
podman login quay.io --authfile ../auth.json

podman push sistema-backend:$version quay.io/uemcpa/sistema-backend:$version --auth=../auth.json
podman push sistema-backend:latest quay.io/uemcpa/sistema-backend:latest --auth=../auth.json
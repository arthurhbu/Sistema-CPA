#!/bin/bash
version="v$(date +'%Y%m%d')"
# Faz o login para enviar aos repositórios públicos
podman login quay.io --authfile ../auth.json
podman build . -t sistema-backend:latest -t sistema-backend:$version 

podman push sistema-backend:$version quay.io/uemcpa/sistema-backend:$version --authfile ../auth.json
podman push sistema-backend:latest quay.io/uemcpa/sistema-backend:latest --authfile ../auth.json
#!/bin/bash
version="v$(date +'%Y%m%d')"
podman login quay.io --authfile ../auth.json
podman build . -t sistema-frontend:latest -t sistema-frontend:$version 

podman push sistema-frontend:$version quay.io/uemcpa/sistema-frontend:$version --authfile ../auth.json
podman push sistema-frontend:latest quay.io/uemcpa/sistema-frontend:latest --authfile ../auth.json
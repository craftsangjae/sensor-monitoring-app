#!/bin/bash
docker buildx build --push --platform linux/amd64 -t registry.crafthomelab.com/sensor-server:latest .

kubectl rollout restart deployment sensor-server -n sensor
#!/bin/bash
docker buildx build --push --platform linux/amd64 -t registry.crafthomelab.com/sensor-graphql:latest .

kubectl rollout restart deployment sensor-graphql -n sensor

#!/usr/bin/env bash

if [ -f papilot/config.env ]; then
  echo "config.env already exists, skipping"
  echo "Please delete config.env if you want to re-run this script"
  exit 0
fi

echo "Models available:"
echo "[1] codegen-350M-mono (2GB total VRAM required; Python-only)"
echo "[2] codegen-350M-multi (2GB total VRAM required; multi-language)"
echo "[3] codegen-2B-mono (7GB total VRAM required; Python-only)"
echo "[4] codegen-2B-multi (7GB total VRAM required; multi-language)"
echo "[5] codegen-6B-mono (13GB total VRAM required; Python-only)"
echo "[6] codegen-6B-multi (13GB total VRAM required; multi-language)"
echo "[7] codegen-16B-mono (32GB total VRAM required; Python-only)"
echo "[8] codegen-16B-multi (32GB total VRAM required; multi-language)"
# Read their choice
read -p "Enter your choice [1]: " MODEL_NUM

# Convert model number to model name
case $MODEL_NUM in
1) MODEL="Salesforce/codegen-350M-mono" ;;
2) MODEL="Salesforce/codegen-350M-multi" ;;
3) MODEL="Salesforce/codegen-2B-mono" ;;
4) MODEL="Salesforce/codegen-2B-multi" ;;
5) MODEL="Salesforce/codegen-6B-mono" ;;
6) MODEL="Salesforce/codegen-6B-multi	" ;;
7) MODEL="Salesforce/codegen-16B-mono" ;;
8) MODEL="Salesforce/codegen-16B-multi	" ;;
*) MODEL="Salesforce/codegen-350M-mono" ;;
esac

# Read number of GPUs
read -p "Enter number of GPUs [1]: " NUM_GPUS
NUM_GPUS=${NUM_GPUS:-1}

echo "Deployment method:"
echo "[1] Deploy to Docker"
echo "[2] Deploy to localhost"
read -p "Where do you want to deploy the Papilot [localhost]? " DEPLOYMENT
if [ -z "$DEPLOYMENT" ]; then
  DEPLOYMENT="localhost"
fi

read -p "Port [8000]: " PORT
PORT=${PORT:-8000}

echo "lock_max_tokens [16]: " TOKEN_LENGTH
TOKEN_LENGTH=${TOKEN_LENGTH:-16}

# Write config.env
echo "MODEL=${MODEL}" >papilot/config.env
echo "NUM_GPUS=${NUM_GPUS}" >>papilot/config.env
echo "PORT=${PORT}" >>papilot/config.env

if [ "$DEPLOYMENT" == "localhost" ]; then
  echo "Deploying to localhost"
  cd papilot
  echo "install dependencies......"
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  echo "done"
  echo "starting server......"
  python main.py
else
  echo "Deploying to Docker"
fi

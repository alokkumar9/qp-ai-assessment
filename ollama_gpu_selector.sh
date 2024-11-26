#!/bin/bash 
# Validate input 
validate_input() { 
    if [[ ! $1 =~ ^[0-4](,[0-4])*$ ]]; then 
        echo "Error: Invalid input. Please enter numbers between 0 and 4, separated by commas." 
        exit 1 
    fi 
} 

# Update service file with CUDA_VISIBLE_DEVICES values 
update_service() { 
    if grep -q '^Environment="CUDA_VISIBLE_DEVICES=' /etc/systemd/system/ollama.service; then 
        sudo sed -i 's/^Environment="CUDA_VISIBLE_DEVICES=.*/Environment="CUDA_VISIBLE_DEVICES='"$1"'"/' /etc/systemd/system/ollama.service 
    else 
        sudo sed -i '/\[Service\]/a Environment="CUDA_VISIBLE_DEVICES='"$1"'"' /etc/systemd/system/ollama.service 
    fi 
    sudo systemctl daemon-reload 
    sudo systemctl restart ollama.service 
    echo "Service updated and restarted with CUDA_VISIBLE_DEVICES=$1" 
} 

if [ "$#" -eq 0 ]; then 
    read -p "Enter CUDA_VISIBLE_DEVICES values (0-4, comma-separated): " cuda_values 
    validate_input "$cuda_values" 
    update_service "$cuda_values" 
else 
    cuda_values="$1" 
    validate_input "$cuda_values" 
    update_service "$cuda_values" 
fi

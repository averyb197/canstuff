#!/bin/bash

if ! pgrep -u "$USER" ssh-agent > /dev/null; then
    echo "Starting SSH agent..."
    eval "$(ssh-agent -s)"
else
    echo "SSH agent is already running."
fi

KEY_PATH="$HOME/.ssh/gitbutt"  
if [[ -f "$KEY_PATH" ]]; then
    ssh-add "$KEY_PATH"
    echo "Added SSH key: $KEY_PATH"
else
    echo "Error: SSH key not found at $KEY_PATH"
    exit 1
fi

echo "Testing SSH connection to GitHub..."
ssh -T git@github.com

if [[ $? -eq 1 ]]; then
    echo "SSH connection successful! Your key is properly set up."
else
    echo "Error: SSH connection failed. Check your SSH key and configuration."
    exit 1
fi

echo "Exporting SSH agent environment variables..."
export SSH_AGENT_PID
export SSH_AUTH_SOCK

echo "SSH setup complete and persistent for this session."




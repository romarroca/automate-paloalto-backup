#!/bin/bash

# First request: Get the key. Change this value to your environment
usern="admin"
passwd="admin"
ipaddr="10.1.1.1"

response=$(curl -sk "https://${ipaddr}/api/?type=keygen&user=${usern}&password=${passwd}")

# Extract the key using grep and sed (or XML parsing with awk)
key=$(echo "$response" | grep -oP '(?<=<key>).*?(?=</key>)')

# Check if the key was extracted
if [ -n "$key" ]; then
    echo "Extract key successful."

    # Generate filename with date-time format (YYYYMMDD_HHMMSS)
    timestamp=$(date +"%Y%m%d_%H%M%S")
    filename="date_$timestamp.tgz"

    # Second request: Use the extracted key and save output to file
    curl -sk "https://${ipaddr}/api/?type=export&category=device-state&key=$key" -o "/somepath/${filename}"

    echo "Configuration backup saved as: $filename"
else
    echo "Failed to extract key."
fi
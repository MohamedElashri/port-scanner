#!/bin/bash

# Set the installation directory
INSTALL_DIR="/opt/port-scanner"

# Set the systemd service file path
SERVICE_FILE="/etc/systemd/system/port-scanner.service"

# Check if the systemd service exists and stop it if it does
if systemctl is-active --quiet port-scanner.service; then
    echo "Stopping Port Scanner Service..."
    sudo systemctl stop port-scanner.service
fi

# Disable the service to not start on boot
if systemctl is-enabled --quiet port-scanner.service; then
    echo "Disabling Port Scanner Service..."
    sudo systemctl disable port-scanner.service
fi

# Check if the systemd service file exists and delete it
if [ -f "$SERVICE_FILE" ]; then
    echo "Removing systemd service file..."
    sudo rm "$SERVICE_FILE"
fi

# Reload systemd to update the changes
sudo systemctl daemon-reload

# Remove the installation directory
echo "Removing installation directory..."
sudo rm -rf "$INSTALL_DIR"

# Remove the user created for the service
echo "Removing service user 'port_scanner'..."
sudo userdel -r port_scanner

# Output completion
echo "Port Scanner Service has been uninstalled."
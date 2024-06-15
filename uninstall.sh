#!/bin/bash

# Set the installation directory
INSTALL_DIR="/opt/port-scanner"

# Stop and disable the Port Scanner Service
sudo systemctl stop port-scanner.service
sudo systemctl disable port-scanner.service

# Remove the systemd service file
sudo rm -f /etc/systemd/system/port-scanner.service

# Reload the systemd daemon
sudo systemctl daemon-reload

# Remove the dedicated user
sudo userdel -r port_scanner

# Remove the setcap capability from Python
sudo setcap -r $(which python3)

# Remove the installation directory and its contents
sudo rm -rf "$INSTALL_DIR"

echo "Port Scanner Service uninstallation completed."
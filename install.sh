#!/bin/bash

# Set the installation directory
INSTALL_DIR="/opt/port-scanner"

# Check if the installation directory exists and prompt for re-installation
if [ -d "$INSTALL_DIR" ]; then
    read -p "Installation directory $INSTALL_DIR already exists. Do you want to reinstall? (y/n): " reinstall
    if [[ "$reinstall" != "y" ]]; then
        echo "Re-installation aborted."
        exit 0
    fi
fi

# Create the installation directory
sudo mkdir -p "$INSTALL_DIR"

# Create or update the virtual environment
if [ -d "$INSTALL_DIR/venv" ]; then
    echo "Using existing virtual environment."
else
    python3 -m venv "$INSTALL_DIR/venv"
fi
source "$INSTALL_DIR/venv/bin/activate"

# Install dependencies
pip install -r requirements.txt

# Copy the port_scanner.py script to the installation directory
cp port_scanner.py "$INSTALL_DIR/"

# Create or update the dedicated user for running the service
if id "port_scanner" &>/dev/null; then
    echo "User port_scanner already exists."
else
    sudo useradd -mr -s /bin/false -d "$INSTALL_DIR" port_scanner
    sudo usermod -aG docker port_scanner
fi

# Adjust ownership of the installation directory
sudo chown -R port_scanner:port_scanner "$INSTALL_DIR"

# Create or update the dedicated log directory within /var/log
LOG_DIR="/var/log/port-scanner"
sudo mkdir -p "$LOG_DIR"
sudo chown port_scanner:port_scanner "$LOG_DIR"

# Adjust the log file path in the Python script
LOG_FILE="$LOG_DIR/port-scan.log"
sed -i "s|/var/log/port-scan.log|$LOG_FILE|g" "$INSTALL_DIR/port_scanner.py"

# Generate the systemd service file
cat > port-scanner.service <<EOL
[Unit]
Description=Port Scanner Service
After=network.target

[Service]
Environment="PATH=$INSTALL_DIR/venv/bin"
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/port_scanner.py
Restart=always
User=port_scanner
WorkingDirectory=$INSTALL_DIR
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOL

# Move the generated service file to the systemd directory
sudo mv port-scanner.service /etc/systemd/system/

# Reload the systemd daemon
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable port-scanner.service
sudo systemctl start port-scanner.service

echo "Port Scanner Service installation completed."
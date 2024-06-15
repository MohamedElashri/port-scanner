#!/bin/bash

# Set the installation directory
INSTALL_DIR="/opt/port-scanner"

# Create the installation directory
if [ ! -d "$INSTALL_DIR" ]; then
    sudo mkdir -p "$INSTALL_DIR"
fi

# Create a virtual environment
if [ -d "$INSTALL_DIR/venv" ]; then
    source "$INSTALL_DIR/venv/bin/activate"
else
    python3 -m venv "$INSTALL_DIR/venv"
    source "$INSTALL_DIR/venv/bin/activate"
fi

# Install dependencies
pip install -r requirements.txt

# Copy the port_scanner.py script to the installation directory
cp port_scanner.py "$INSTALL_DIR/"

# Create a dedicated user for running the service
if ! id -u port_scanner > /dev/null 2>&1; then
    sudo useradd -m -s /bin/false port_scanner
fi

# Grant necessary permissions to the port_scanner user
sudo usermod -aG docker port_scanner

# Find the actual Python executable path
PYTHON_EXEC=$(readlink -f "$(which python3)")

# Set capabilities on the actual Python executable
sudo setcap 'cap_net_raw,cap_net_admin+eip' "$PYTHON_EXEC"

# Generate the systemd service file
cat > port-scanner.service <<EOL
[Unit]
Description=Port Scanner Service
After=network.target

[Service]
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/port_scanner.py
Restart=always
User=port_scanner

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
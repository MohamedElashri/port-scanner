
# Port Scanner Service

The Port Scanner Service is a Python script that scans for open ports on the local machine, determines if the ports are used by Docker containers or other services, and presents the information in a colorful table. It also humorously insults the user if any ports other than 80 and 443 are open. The script supports optional Telegram bot and email notifications for detected open ports.

## Features

- Scans for open ports on the local machine
- Determines if ports are used by Docker containers or other services
- Presents the results in a colorful table
- Sends humorous insult via Telegram bot and email if non-standard ports are open
- Supports customizable scanning schedule (hourly, daily, weekly)
- Allows specifying ports to scan or skip
- Logs interesting events and timestamps to a log file

## Prerequisites

- Python 3.x
- Docker (if you want to detect ports used by Docker containers)
- Telegram bot token and chat ID (if you want to use Telegram notifications)
- SMTP server credentials (if you want to use email notifications)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/MohamedElashri/port-scanner
   cd port-scanner
   ```

2. Create a `.env` file in the project directory and provide the necessary configuration values:
   ```
   # Telegram bot integration (optional)
   USE_TELEGRAM_BOT=False
   TELEGRAM_BOT_TOKEN='YOUR_BOT_TOKEN'
   TELEGRAM_CHAT_ID='YOUR_CHAT_ID'

   # Email notification settings
   USE_EMAIL_NOTIFICATION=False
   SMTP_SERVER='YOUR_SMTP_SERVER'
   SMTP_PORT=587
   SMTP_USERNAME='YOUR_EMAIL_USERNAME'
   SMTP_PASSWORD='YOUR_EMAIL_PASSWORD'
   EMAIL_SENDER='sender@example.com'
   EMAIL_RECIPIENT='recipient@example.com'

   # Scan configuration
   SCAN_SCHEDULE='hourly'
   PORTS_TO_SCAN=''
   PORTS_TO_SKIP=''
   ```

   Modify the values according to your setup and preferences.

3. Run the installation script:
   ```
   chmod +x install.sh
   ./install.sh
   ```

   The script will set up a virtual environment, install dependencies, create a dedicated user, grant necessary permissions, and set up the systemd service.

4. The Port Scanner Service will start automatically after installation. You can check its status using:
   ```
   sudo systemctl status port-scanner.service
   ```

## Usage

The Port Scanner Service runs automatically based on the configured scanning schedule. It will scan for open ports, determine the associated services, and log the results to the specified log file.

If any non-standard ports (other than 80 and 443) are detected, the script will send a humorous insult message via Telegram bot and email, depending on the configured notification settings.

You can customize the scanning behavior by modifying the relevant variables in the `.env` file:
- `SCAN_SCHEDULE`: Set the scanning frequency (`hourly`, `daily`, `weekly`).
- `PORTS_TO_SCAN`: Specify the ports to scan (comma-separated). Leave empty to scan all ports.
- `PORTS_TO_SKIP`: Specify the ports to skip (comma-separated).

## Uninstallation

To uninstall the Port Scanner Service, run the uninstallation script:
```
chmod +x uninstall.sh
./uninstall.sh
```

The script will stop the service, remove the systemd unit file, delete the dedicated user, and remove the virtual environment.

## Logs

The script logs interesting events and timestamps to the log file located at `/var/log/port-scan.log`. You can view the logs using a command like:
```
tail -f /var/log/port-scan.log
```

## License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE).


import os
import subprocess
import prettytable
from colorama import Fore, Style
import telegram
from telegram.ext import Updater, CommandHandler
import socket
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram bot integration (optional)
USE_TELEGRAM_BOT = os.getenv('USE_TELEGRAM_BOT', 'False').lower() == 'true'
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Email notification settings
USE_EMAIL_NOTIFICATION = os.getenv('USE_EMAIL_NOTIFICATION', 'False').lower() == 'true'
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')

# Logging configuration
LOG_FILE = '/var/log/port-scan.log'
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# Scan configuration
SCAN_SCHEDULE = os.getenv('SCAN_SCHEDULE', 'hourly')
PORTS_TO_SCAN = os.getenv('PORTS_TO_SCAN', '').split(',')
PORTS_TO_SKIP = os.getenv('PORTS_TO_SKIP', '').split(',')

def get_hostname():
    return socket.gethostname()

def get_external_ip():
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return 'Unknown'

def scan_ports():
    open_ports = []
    docker_ports = set()

    # Get Docker container open ports
    try:
        output = subprocess.check_output(['docker', 'ps', '--format', '{{.Ports}}'])
        docker_output = output.decode('utf-8').strip().split('\n')
        for line in docker_output:
            ports = line.split('->')
            if len(ports) > 1:
                docker_ports.add(ports[0].split(':')[1])
    except subprocess.CalledProcessError:
        pass

    # Scan for open ports
    for port in range(1, 65536):
        if PORTS_TO_SCAN and str(port) not in PORTS_TO_SCAN:
            continue
        if str(port) in PORTS_TO_SKIP:
            continue

        result = os.system(f'nc -z -w1 localhost {port} > /dev/null 2>&1')
        if result == 0:
            service = 'Docker' if str(port) in docker_ports else 'Other'
            open_ports.append([port, service])

    return open_ports

def create_table(open_ports):
    table = prettytable.PrettyTable()
    table.field_names = ['Port', 'Service']
    for port, service in open_ports:
        if port in [80, 443]:
            table.add_row([Fore.GREEN + str(port) + Style.RESET_ALL, service])
        else:
            table.add_row([Fore.RED + str(port) + Style.RESET_ALL, service])
    return table

def send_telegram_message(message):
    if USE_TELEGRAM_BOT:
        try:
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        except Exception as e:
            logging.error(f'Error sending Telegram message: {e}')

def send_email_notification(subject, message):
    if USE_EMAIL_NOTIFICATION:
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_SENDER
            msg['To'] = EMAIL_RECIPIENT
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
        except Exception as e:
            logging.error(f'Error sending email notification: {e}')

def scan_and_notify():
    hostname = get_hostname()
    external_ip = get_external_ip()

    open_ports = scan_ports()
    table = create_table(open_ports)

    logging.info(f'Port scan results for {hostname} ({external_ip}):\n{table}')

    non_standard_ports = [port for port, _ in open_ports if port not in [80, 443]]
    if non_standard_ports:
        insult = f"Hey dummy, why do you have these weird ports open on {hostname} ({external_ip}): {', '.join(map(str, non_standard_ports))}? Are you trying to invite hackers to your party? 🤡"
        logging.warning(insult)
        send_telegram_message(insult)
        send_email_notification('Open Ports Detected', insult)

def scheduled_scan():
    logging.info('Starting scheduled port scan')
    scan_and_notify()
    logging.info('Scheduled port scan completed')

def main():
    # Configure logging
    handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_SIZE, backupCount=LOG_BACKUP_COUNT)
    logging.basicConfig(handlers=[handler], level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Schedule the scan
    if SCAN_SCHEDULE == 'hourly':
        schedule.every().hour.do(scheduled_scan)
    elif SCAN_SCHEDULE == 'daily':
        schedule.every().day.do(scheduled_scan)
    elif SCAN_SCHEDULE == 'weekly':
        schedule.every().week.do(scheduled_scan)

    logging.info('Port Scanner Service started')

    # Run the scheduled scans indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
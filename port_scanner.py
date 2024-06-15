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

# Rest of the script code remains the same
"""
CLI Commands Cit Citas Send Messages
"""
from datetime import datetime, timedelta
import locale
import os

from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail
from tabulate import tabulate

# Region
locale.setlocale(locale.LC_TIME, "es_MX.utf8")

# SendGrid environment variables
load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "")

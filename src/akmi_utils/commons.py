import logging
import os
import tomli

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_project_details(base_dir: str, keys: list):
    with open(os.path.join(base_dir, 'pyproject.toml'), 'rb') as file:
        package_details = tomli.load(file)
    poetry = package_details['project']
    return {key: poetry[key] for key in keys}


def send_gmail(subject: str, body: str, app_settings=None):
    mail_usr = app_settings.mail_usr
    mail_pass = app_settings.mail_pass
    mail_to = app_settings.mail_to
    msg = MIMEMultipart()
    msg['From'] = mail_usr
    msg['To'] = ', '.join(mail_to)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(mail_usr, mail_pass)
            server.sendmail(mail_usr, mail_to, msg.as_string())
        print("Email sent successfully.")
        logging.info("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        logging.error(f"Failed to send email: {e}")
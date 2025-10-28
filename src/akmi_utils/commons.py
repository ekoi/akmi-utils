import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging.handlers import TimedRotatingFileHandler

import tomli
from dynaconf import Dynaconf

base_project_dir = os.getenv("BASE_DIR", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
build_date = os.environ.get("BUILD_DATE", "unknown")


# build absolute paths for Dynaconf using base_dir
settings_files = [
    os.path.join(base_project_dir, "conf", "settings.toml"),
    os.path.join(base_project_dir, "conf", "*.yaml"),
    os.path.join(base_project_dir, "conf", ".secrets.toml"),
]

app_settings = Dynaconf(
    settings_files=settings_files,
    environments=True,
    root_path=base_project_dir,
)

log_file = app_settings.get("log_file", "akmi.log")

handler = TimedRotatingFileHandler(
    log_file,
    when="midnight",  # rotate every second for testing
    interval=1,
    backupCount=7,
    encoding="utf-8",
    utc=True
)
handler.suffix = "%Y-%m-%d"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[handler]
)

def get_project_details(keys: list, base_dir: str | None = None) -> dict:
    if base_dir is None:
        base_dir = base_project_dir

    if not isinstance(keys, (list, tuple)):
        raise TypeError("`keys` must be a list or tuple of keys to retrieve")

    pyproject_path = os.path.join(base_dir, 'pyproject.toml')
    if not os.path.exists(pyproject_path):
        raise FileNotFoundError(f"`pyproject.toml` not found at `{pyproject_path}`")

    with open(pyproject_path, 'rb') as file:
        package_details = tomli.load(file)

    project = package_details.get('project')
    if project is None:
        raise KeyError("No `project` table found in `pyproject.toml`")

    missing = [k for k in keys if k not in project]
    if missing:
        raise KeyError(f"Missing keys in `project`: {missing}")

    return {key: project[key] for key in keys}


def send_gmail(subject: str, body: str):
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
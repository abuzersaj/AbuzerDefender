import os
import yara
import logging
import psutil
import smtplib
import configparser
from email.message import EmailMessage
import time

logging.basicConfig(filename="abuzer_defender.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Created by Abuzer - Real-Time Monitoring Active")

def send_email_alert(subject, body):
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = config['EMAIL']['FROM']
        msg['To'] = config['EMAIL']['TO']

        with smtplib.SMTP_SSL(config['EMAIL']['SMTP_SERVER'], int(config['EMAIL']['PORT'])) as smtp:
            smtp.login(config['EMAIL']['FROM'], config['EMAIL']['PASSWORD'])
            smtp.send_message(msg)
        logging.info("Email alert sent.")
    except Exception as e:
        logging.error(f"Email alert failed: {e}")

def yara_scan_folder(folder_path):
    try:
        rules = yara.compile(filepath="malware_rules.yar")
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    matches = rules.match(file_path)
                    if matches:
                        msg = f"🚨 YARA matched: {file_path} - {matches}"
                        logging.warning(msg)
                        send_email_alert("🚨 AbuzerDefender Alert", msg)
                except Exception:
                    continue
    except Exception as e:
        logging.error(f"YARA error: {e}")

def monitor_processes():
    seen = set()
    while True:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.pid not in seen:
                seen.add(proc.pid)
                pname = proc.info['name'].lower()
                if any(x in pname for x in ['powershell', 'cmd', 'wscript']):
                    msg = f"⚠️ Suspicious process: {pname} (PID {proc.pid})"
                    logging.warning(msg)
                    send_email_alert("⚠️ AbuzerDefender Process Alert", msg)
        time.sleep(5)

if __name__ == "__main__":
    print("AbuzerDefender AI - Monitoring started...")
    yara_scan_folder("D:\\\\Downloads")
    monitor_processes()

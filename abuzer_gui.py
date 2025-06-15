import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import time
import logging
import psutil
import configparser
import smtplib
from email.message import EmailMessage

# Set up logging to console + file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Global flag to control monitoring loop
monitoring = False

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
        log_to_gui("INFO", "Email alert sent.")
    except Exception as e:
        log_to_gui("ERROR", f"Email alert failed: {e}")

def log_to_gui(level, message):
    # Insert message to GUI log window (thread-safe)
    gui_log.config(state='normal')
    gui_log.insert(tk.END, f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {level} - {message}\n")
    gui_log.see(tk.END)
    gui_log.config(state='disabled')

def monitor_processes():
    global monitoring
    seen = set()
    while monitoring:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.pid not in seen:
                seen.add(proc.pid)
                pname = proc.info['name'].lower()
                if any(x in pname for x in ['powershell', 'cmd', 'wscript']):
                    msg = f"⚠️ Suspicious process: {pname} (PID {proc.pid})"
                    logging.warning(msg)
                    log_to_gui("WARNING", msg)
                    send_email_alert("⚠️ AbuzerDefender Process Alert", msg)
        time.sleep(5)
    log_to_gui("INFO", "Monitoring stopped.")

def start_monitoring():
    global monitoring
    if not monitoring:
        monitoring = True
        log_to_gui("INFO", "Starting process monitoring...")
        threading.Thread(target=monitor_processes, daemon=True).start()

def stop_monitoring():
    global monitoring
    monitoring = False

# GUI setup
root = tk.Tk()
root.title("AbuzerDefender AI - GUI")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

start_btn = tk.Button(frame, text="Start Monitoring", command=start_monitoring)
start_btn.grid(row=0, column=0, padx=5)

stop_btn = tk.Button(frame, text="Stop Monitoring", command=stop_monitoring)
stop_btn.grid(row=0, column=1, padx=5)

gui_log = ScrolledText(root, width=80, height=20, state='disabled')
gui_log.pack(padx=10, pady=10)

root.mainloop()

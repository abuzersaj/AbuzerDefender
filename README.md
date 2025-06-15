# AbuzerDefender

AI-powered real-time malware detection and monitoring tool built with Python, YARA rules, and a Flask dashboard.

---

## 🚀 Features

- Real-time process monitoring on Windows
- Malware scanning using YARA signatures
- Email alerts for suspicious activity
- Interactive Flask dashboard to view logs live
- Easy-to-configure via `config.ini`

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/abuzersaj/AbuzerDefender.git
cd AbuzerDefender

2.Create and activate virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # macOS/Linux

3.Install dependencies
pip install -r requirements.txt

4. Configure your email alerts
Rename config.sample.ini to config.ini

Edit the file and add your Gmail address, app password, and recipient email

How to Run
Start the malware monitoring script
python abuzer_defender.py

(Optional) Start the Flask dashboard
python dashboard.py

Then open your browser at:
http://127.0.0.1:8080


 Contribution
Contributions and suggestions are welcome!
Please open issues for bugs or feature requests.
Pull requests are encouraged.

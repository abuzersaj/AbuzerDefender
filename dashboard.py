from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def show_logs():
    try:
        with open("abuzer_defender.log", "r") as f:
            logs = f.read()
    except:
        logs = "No log file found."

    return render_template_string(f"""
    <html>
    <head><title>AbuzerDefender Logs</title></head>
    <body style='font-family: monospace; background-color: #121212; color: #33FF57;'>
        <h1>AbuzerDefender AI - Logs</h1>
        <pre>{logs}</pre>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, port=8080)

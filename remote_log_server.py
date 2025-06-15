from flask import Flask, request

app = Flask(__name__)

@app.route('/upload_log', methods=['POST'])
def upload_log():
    log_data = request.data.decode()
    with open("central_logs.txt", "a") as f:
        f.write(log_data + "\n")
    return "Log received", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

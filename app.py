from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HTML_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Form Submission</title>
</head>
<body>
    <h2>Form 1</h2>
    <form action="/submit" method="post">
        <input type="hidden" name="form" value="form1">
        Name: <input type="text" name="name"><br>
        Email: <input type="email" name="email"><br>
        <input type="submit" value="Submit Form 1">
    </form>
    <hr>
    <h2>Form 2</h2>
    <form action="/submit" method="post">
        <input type="hidden" name="form" value="form2">
        Username: <input type="text" name="username"><br>
        Message: <input type="text" name="message"><br>
        <input type="submit" value="Submit Form 2">
    </form>
</body>
</html>
'''

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_FORM)

@app.route("/submit", methods=["POST"])
def submit():
    form_type = request.form.get("form")
    data = request.form.to_dict()
    message = f"New submission from {form_type}:\n" + "\n".join([f"{k}: {v}" for k, v in data.items() if k != "form"])

    if form_type == "form1":
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
    elif form_type == "form2":
        token = os.getenv("TELEGRAM_BOT_TOKEN_WEB")
        chat_id = os.getenv("TELEGRAM_CHAT_ID_WEB")
    else:
        return jsonify({"error": "Unknown form type"}), 400

    send_status = send_to_telegram(message, token, chat_id)
    return jsonify({"status": send_status})

def send_to_telegram(text, token, chat_id):
    if not token or not chat_id:
        return "Missing token or chat_id"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)
    return "ok" if response.status_code == 200 else response.text

if __name__ == "__main__":
    app.run(debug=True)

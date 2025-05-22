from flask import Flask, request, jsonify, render_template_string
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HTML_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Form Submission</title>
</head>
<body>
    <h2>Форма 1</h2>
    <form action="/submit" method="post">
        <input type="hidden" name="form" value="form1">
        <label>Ваше имя*:</label>
        <input type="text" name="full_name" placeholder="Введите ваше имя"><br>
        <label>Контактные данные (WhatsApp/Telegram)*:</label>
        <input type="text" name="contact" placeholder="@username или номер телефона"><br>
        <label>Комментарий*:</label>
        <textarea name="comment" placeholder="Введите комментарий"></textarea><br>
        <input type="submit" value="Отправить форму 1">
    </form>

    <hr>

    <h2>Форма 2</h2>
    <form action="/submit" method="post">
        <input type="hidden" name="form" value="form2">
        <label>Ваше имя*:</label>
        <input type="text" name="full_name" placeholder="Введите ваше имя"><br>
        <label>Контактные данные (WhatsApp/Telegram)*:</label>
        <input type="text" name="contact" placeholder="@username или номер телефона"><br>
        <label>Комментарий*:</label>
        <textarea name="comment" placeholder="Введите комментарий"></textarea><br>
        <input type="submit" value="Отправить форму 2">
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
    message = f"Новая заявка с {form_type}:\n" + "\n".join([f"{k}: {v}" for k, v in data.items() if k != "form"])

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
    app.run(debug=True, host="0.0.0.0", port=5000)

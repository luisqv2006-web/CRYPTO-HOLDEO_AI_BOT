from flask import Flask, render_template_string
import datetime

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Crypto Oráculo VIP</title>
    <style>
        body { background-color: #0d0d0d; color: #ffffff; font-family: Arial; text-align: center; }
        h1 { color: #d4af37; margin-top: 40px; }
        .box {
            background: #1a1a1a; border: 1px solid #d4af37;
            padding: 20px; margin: 30px auto;
            width: 70%; border-radius: 12px;
        }
        .footer { margin-top: 50px; color: #777; font-size: 14px; }
    </style>
</head>
<body>

<h1>CRYPTO ORÁCULO — PANEL VIP</h1>

<div class="box">
    <p><strong>Estado del sistema:</strong> ONLINE 🟢</p>
    <p><strong>Worker:</strong> Ejecutándose en segundo plano ⚙️</p>
    <p><strong>Última actualización:</strong> {{ time }}</p>
</div>

<div class="footer">
    © Crypto Oráculo VIP — Powered by Day & Érica
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(TEMPLATE, time=datetime.datetime.utcnow())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

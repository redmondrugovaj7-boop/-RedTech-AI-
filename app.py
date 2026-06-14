import os
import requests
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)

import os

# Merr çelësin në mënyrë të sigurt nga Vercel
CHILESI_SEKRET = os.environ.get('GEMINI_API_KEY')

# Rregullat bazë të AI
rregullat = "Je RedTech AI, një asistent inteligjent."

# Lexon rregullat.txt nëse ekziston
if os.path.exists("rregullat.txt"):
    try:
        with open("rregullat.txt", "r", encoding="utf-8") as f:
            rregullat = f.read()
    except Exception as e:
        print(f"Gabim gjatë leximit të rregullave: {e}")

# Faqja kryesore
@app.route('/')
def home():
    response = make_response(render_template('index.html'))
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

# API për mesazhe
@app.route('/dergo', methods=['POST'])
def dergo_mesazh():
    try:
        te_dhenat = request.get_json()
        pyetja = te_dhenat.get("mesazhi", "")

        if not pyetja.strip():
            return jsonify({
                "pergjigja": "Ju lutem shkruani diçka..."
            })

        # URL zyrtare për Gemini AI në vitin 2026
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={CHILESI_SEKRET}"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{rregullat}\n\nUser: {pyetja}"
                        }
                    ]
                }
            ]
        }

        # Dërgon kërkesën
        req = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        res = req.json()

        # Merr përgjigjen ose tregon gabimin e saktë
        if "candidates" in res and len(res["candidates"]) > 0:
            teksti = res["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({
                "pergjigja": teksti
            })
        elif "error" in res:
            return jsonify({
                "pergjigja": f"Gabim nga Google: {res['error']['message']}"
            })
        else:
            return jsonify({
                "pergjigja": "Nuk mora përgjigje të saktë nga AI."
            })

    except Exception as e:
        return jsonify({
            "pergjigja": f"Gabim gjatë dërgimit: {str(e)}"
        })

# Nis serverin
if __name__ == '__main__':
    porti = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=porti, debug=True)

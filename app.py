import os
import requests
from flask import Flask, render_template, request, jsonify, make_response
from dotenv import load_dotenv

# Ngarkon .env
load_dotenv()

app = Flask(__name__)

# Merr API KEY nga .env
CHILESI_SEKRET = os.getenv("GEMINI_API_KEY")

rregullat = "Je RedTech AI, një asistent inteligjent."

if os.path.exists("rregullat.txt"):
    try:
        with open("rregullat.txt", "r", encoding="utf-8") as f:
            rregullat = f.read()
    except Exception as e:
        print(f"Gabim: {e}")

@app.route('/')
def home():
    response = make_response(render_template('index.html'))
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

@app.route('/dergo', methods=['POST'])
def dergo_mesazh():
    try:
        te_dhenat = request.get_json()

        pyetja = te_dhenat.get("mesazhi", "")

        if not pyetja.strip():
            return jsonify({
                "pergjigja": "Ju lutem shkruani diçka..."
            })

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

        req = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        res = req.json()

        print(res)

        if "candidates" in res:
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
                "pergjigja": "Nuk mora përgjigje nga AI."
            })

    except Exception as e:
        return jsonify({
            "pergjigja": f"Gabim gjatë dërgimit: {str(e)}"
        })

if __name__ == '__main__':
    porti = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=porti, debug=True)

import os
import requests
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)

# Çelësi sekret i gatshëm direkt në kod
CHILESI_SEKRET = "AIzaSyCzkok647fu7aOYFch77fVIHQeRUbvcstg"

# Lexohen rregullat në mënyrë të sigurt
rregullat = "Je RedTech AI, një asistent inteligjent."
if os.path.exists("rregullat.txt"):
    try:
        with open("rregullat.txt", "r", encoding="utf-8") as f:
            rregullat = f.read()
    except Exception as e:
        print(f"Gabim gjatë leximit të rregullat.txt: {e}")

@app.route('/')
def home():
    response = make_response(render_template('index.html'))
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

@app.route('/dergo', methods=['POST'])
def dergo_mesazh():
    te_dhenat = request.json
    pyetja = te_dhenat.get("mesazhi", "")
    
    if not pyetja.strip():
        return jsonify({"pergjigja": "Ju lutem shkruani diçka..."})
        
    # Kemi ndryshuar modelin në gemini-1.5-flash-8b që është i certifikuar për API v1
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-8b:generateContent?key={CHILESI_SEKRET}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Rregullat e sistemit që duhet t'i zbatosh me ngulm:\n{rregullat}\n\nMesazhi i përdoruesit: {pyetja}"}
                ]
            }
        ]
    }
    
    try:
        REDEPLOY_REQ = requests.post(url, json=payload, headers=headers)
        pergjigja_json = REDEPLOY_REQ.json()
        
        if "candidates" in pergjigja_json:
            teksti = pergjigja_json["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"pergjigja": teksti})
        else:
            return jsonify({"pergjigja": f"Gabim nga Google: {pergjigja_json}"})
            
    except Exception as e:
        return jsonify({"pergjigja": f"Gabim gjatë dërgimit: {e}"})

if __name__ == '__main__':
    porti = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=porti)

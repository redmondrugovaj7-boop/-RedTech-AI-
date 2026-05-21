import os
import requests
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)

CHILESI_SEKRET = "AIzaSyCzkok647fu7aOYFch77fVIHQeRUbvcstg"

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
    te_dhenat = request.json
    pyetja = te_dhenat.get("mesazhi", "")
    
    if not pyetja.strip():
        return jsonify({"pergjigja": "Ju lutem shkruani diçka..."})
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={CHILESI_SEKRET}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": f"{rregullat}\n\nUser: {pyetja}"}]
        }]
    }
    
    try:
        req = requests.post(url, json=payload, headers=headers)
        res = req.json()
        if "candidates" in res:
            teksti = res["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"pergjigja": teksti})
        else:
            return jsonify({"pergjigja": f"Gabim: {res}"})
    except Exception as e:
        return jsonify({"pergjigja": f"Gabim: {e}"})

if __name__ == '__main__':
    porti = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=porti)

import os
import sys
from flask import Flask, render_template, request, jsonify, make_response
from google import genai
from google.genai import types

app = Flask(__name__)

CHILESI_SEKRET = "AIzaSyCzkok647fu7aOYFch77fVIHQeRUbvcstg"

try:
    client = genai.Client(api_key=CHILESI_SEKRET)
    with open("rregullat.txt", "r", encoding="utf-8") as f:
        rregullat = f.read()
except Exception as e:
    print(f"Gabim gjatë nisjes: {e}")
    sys.exit()

biseda = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=rregullat,
        temperature=0.7,
    )
)

@app.route('/')
def home():
    # Kjo pjesë e heq faqen e kaltër të Ngrok-ut që babi dhe shokët të futen direkt!
    response = make_response(render_template('index.html'))
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

@app.route('/dergo', methods=['POST'])
def dergo_mesazh():
    te_dhenat = request.json
    pyetja = te_dhenat.get("mesazhi", "")
    
    if not pyetja.strip():
        return jsonify({"pergjigja": "Ju lutem shkruani diçka..."})
        
    try:
        pergjigja = biseda.send_message(pyetja)
        return jsonify({"pergjigja": pergjigja.text})
    except Exception as e:
        return jsonify({"pergjigja": f"Gabim: {e}"})

if __name__ == '__main__':
    print("Faqja e RedTech AI po ndizet...")
    app.run(debug=True, port=5000)
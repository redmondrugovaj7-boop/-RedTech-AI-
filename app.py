import os
from flask import Flask, render_template, request, jsonify, make_response
import google.generativeai as genai

app = Flask(__name__)

CHILESI_SEKRET = "AIzaSyCzkok647fu7aOYFch77fVIHQeRUbvcstg"

# Konfigurohet çelësi sekret i Gemini
genai.configure(api_key=CHILESI_SEKRET)

# Lexohen rregullat në mënyrë të sigurt
rregullat = "Je RedTech AI, një asistent inteligjent."
if os.path.exists("rregullat.txt"):
    try:
        with open("rregullat.txt", "r", encoding="utf-8") as f:
            rregullat = f.read()
    except Exception as e:
        print(f"Gabim gjatë leximit të rregullat.txt: {e}")

# Krijojmë modelin e bisedës me gemini-pro
try:
    model = genai.GenerativeModel(
        model_name="gemini-pro"
    )
    # Pasi gemini-pro i vjetër nuk e ka system_instruction direkt, 
    # ne ia dërgojmë rregullat si mesazh të parë në histori që t'i mbajë mend
    biseda = model.start_chat(history=[
        {"role": "user", "parts": [f"Rregullat e tuaja: {rregullat} Shkruaj 'Kuptova'."]},
        {"role": "model", "parts": ["Kuptova."]}
    ])
except Exception as e:
    print(f"Gabim gjatë krijimit të modelit: {e}")
    biseda = None

@app.route('/')
def home():
    response = make_response(render_template('index.html'))
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

@app.route('/dergo', methods=['POST'])
def dergo_mesazh():
    global biseda
    te_dhenat = request.json
    pyetja = te_dhenat.get("mesazhi", "")
    
    if not pyetja.strip():
        return jsonify({"pergjigja": "Ju lutem shkruani diçka..."})
        
    try:
        if biseda is None:
            model = genai.GenerativeModel(model_name="gemini-pro")
            biseda = model.start_chat(history=[
                {"role": "user", "parts": [f"Rregullat e tuaja: {rregullat} Shkruaj 'Kuptova'."]},
                {"role": "model", "parts": ["Kuptova."]}
            ])
            
        pergjigja = biseda.send_message(pyetja)
        return jsonify({"pergjigja": pergjigja.text})
    except Exception as e:
        return jsonify({"pergjigja": f"Gabim gjatë dërgimit: {e}"})

if __name__ == '__main__':
    porti = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=porti)

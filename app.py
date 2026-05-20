import os
from flask import Flask, render_template, request, jsonify, make_response
from google import genai  # Importi standard dhe i pastër

app = Flask(__name__)

CHILESI_SEKRET = "AIzaSyCzkok647fu7aOYFch77fVIHQeRUbvcstg"

# Ndizet klienti i ri në mënyrë standarde
client = genai.Client(api_key=CHILESI_SEKRET)

# Lexohen rregullat në mënyrë të sigurt
rregullat = "Je RedTech AI, një asistent inteligjent."
if os.path.exists("rregullat.txt"):
    try:
        with open("rregullat.txt", "r", encoding="utf-8") as f:
            rregullat = f.read()
    except Exception as e:
        print(f"Gabim gjatë leximit të rregullat.txt: {e}")

# Krijojmë bisedën me modelin më të ri Gemini 2.5
biseda = None
try:
    biseda = client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": rregullat, "temperature": 0.7}
    )
except Exception as e:
    print(f"Gabim gjatë krijimit të bisedës fillestare: {e}")

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
            biseda = client.chats.create(
                model="gemini-2.5-flash",
                config={"system_instruction": rregullat, "temperature": 0.7}
            )
            
        pergjigja = biseda.send_message(pyetja)
        return jsonify({"pergjigja": pergjigja.text})
    except Exception as e:
        return jsonify({"pergjigja": f"Gabim gjatë dërgimit: {e}"})

if __name__ == '__main__':
    porti = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=porti)

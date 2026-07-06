from flask import Flask,render_template,request,jsonify
from google import genai
from PIL import Image
import os

API_KEY = os.getenv("GEMINI_API_KEY")
client=genai.Client(api_key=API_KEY)
app=Flask(__name__)

SYSTEM = """
Eres un médico virtual ético. Realiza un triaje inicial.

Reglas estrictas de respuesta:
- Sé muy breve y directo.
- Máximo 5-6 líneas por respuesta.
- Usa viñetas (-) o números para organizar.
- Ve al grano sin explicaciones largas.
- Nunca des diagnósticos ni recetas.
- Responde en español claro y sencillo.
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/chat")
def chat():
    msg=request.form.get("message","")
    img=request.files.get("image")
    parts=[SYSTEM,msg]
    if img:
        parts.append(Image.open(img.stream))
    r=client.models.generate_content(model="gemini-2.5-flash",contents=parts)
    return jsonify({"reply":r.text})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

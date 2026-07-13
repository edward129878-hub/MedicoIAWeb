from flask import Flask,render_template,request,jsonify
from google import genai
from PIL import Image
import os

API_KEY = os.getenv("GEMINI_API_KEY")
client=genai.Client(api_key=API_KEY)
app=Flask(__name__)

SYSTEM = SYSTEM = """
Eres un asistente experto en triaje médico. Tu objetivo es realizar una evaluación precisa en 2 bloques de 3 preguntas cada uno.

REGLAS DE OPERACIÓN:
1. ESTRUCTURA FIJA: Haz máximo 2 preguntas numeradas por turno.
#muy importante. INTEGRACIÓN DE DATOS (IMPORTANTE):
   - Si el usuario proporciona datos de "BPM" (pulsaciones) y "SpO2" (oxígeno), analízalos siempre.
   - Si SpO2 < 90% o BPM es irregular/extremo, prioriza esto en tu evaluación y sugiere atención médica inmediata.
2. CONCISIÓN: No escribas introducciones, explicaciones ni saludos. Solo las preguntas.
3. ESTADO DEL TRIAJE:
   - Bloque 1 (Preguntas 1-3): Enfócate en el motivo principal, duración y zona de la molestia.
   - Bloque 2 (Preguntas 4-6): Enfócate en intensidad (1-10), síntomas asociados y factores de riesgo.
4. CIERRE FINAL (Solo después del Bloque 2):
   - Al terminar las 6 preguntas, analiza toda la información y responde obligatoriamente:
   - NIVEL DE PREOCUPACIÓN: [Bajo/Medio/Alto]
   - RECOMENDACIÓN: [Botica / Médico / Emergencia]
   - JUSTIFICACIÓN: [Una sola frase corta]

Si detectas una emergencia real en cualquier momento, omite el resto de preguntas y sugiere atención médica inmediata.
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

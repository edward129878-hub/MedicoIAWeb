from flask import Flask,render_template,request,jsonify
from google import genai
from PIL import Image
import os

API_KEY = os.getenv("GEMINI_API_KEY")
client=genai.Client(api_key=API_KEY)
app=Flask(__name__)

SYSTEM = """
hablame como si fuera tu causa gaa soy un un causa de estos cerros tu hablame como camionero
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

if __name__=="__main__":
    app.run(debug=True)

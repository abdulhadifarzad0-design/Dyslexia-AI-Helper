import openai, os
from gtts import gTTS
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, render_template, send_file, session, redirect, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "ngt587642")

audio_dir = os.path.join('static', 'audio')
os.makedirs(audio_dir, exist_ok=True)

openai.api_key = "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"

def simplify_with_openai(text):
    prompt = f"Simplify this text for a dyslexic reader. User short sentences and simpler vocabulary:\n\n{text}"
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0
        )
    return completion.choices[0].message.content

def translate_text_with_openai(text, target_lang_code):
    prompt = (
        f"Translate the following text into {target_lang_code} language:\n\n{text}"
        )
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0,
        )
    return completion.choices[0].message.content.strip()

def generate_audio(text, lang_code):
    filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    file_path = os.path.join(audio_dir, filename)
    tts = gTTS(text, lang=lang_code)
    tts.save(file_path)
    return f"audio/{filename}"

@app.route("/play_audio")
def play_audio():
    audio_path = session.get('audio_file')
    if audio_path and os.path.exists(audio_path):
        return send_file(audio_path, mimetype="audio/mpeg")
    return "Audio not found.", 404

@app.route("/download_audio")
def download_audio():
    audio_path = session.get('audio_file')
    if audio_path and os.path.exists(audio_path):
        return send_file(audio_path, as_attachment=True)
    return "Audio not found."

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/", methods=["GET", "POST"])
def home():
    simplified = ""
    audio_file = None
    original_text = ""
    translated_text = ""

    #Default values
    selected_language = "english"
    selected_font = "default"

    if request.method == "POST":
        input_text = request.form.get("text", "")
        selected_language = request.form.get("language", "english")
        selected_font = request.form.get("font_family", "deafult").lower()

        if 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file.filename:
                input_text = uploaded_file.read().decode("utf-8")

        original_text = input_text
        simplified = simplify_with_openai(input_text)

        LANG_MAP = {
            'english': 'en', 'spanish': 'es', 'french': 'fr', 'german': 'de',
            'italian': 'it', 'portuguese': 'pt', 'russian': 'ru','chinese(simplified)': 'zh-cn',
            'chinese(traditional)': 'zh-tw', 'japanese': 'ja', 'korean': 'ko', 'hindi': 'hi',
            'arabic': 'ar', 'bengali': 'bn', 'turkish': 'tr', 'dutch': 'nl', 'sweidish': 'sv',
            'vietnamese': 'vi', 'polish': 'pt'
            }
        lang_code = LANG_MAP.get(selected_language.lower(), 'en')

        print(selected_language.lower())
        print(lang_code)

        if lang_code == "en":
            translated_text = simplified
        else:
            translated_text = translate_text_with_openai(simplified, target_lang_code=lang_code)

        audio_file = generate_audio(translated_text, lang_code)
        print("audio_file", audio_file)
        session['audio_file'] = audio_file
        session['simplified'] = translated_text
        session['original'] = original_text
        session['language'] = selected_language
        session['font_family'] = selected_font

    print(translated_text) 
    return render_template("dyslexia_page.html",
                           original_text = original_text,
                           simplified = translated_text,
                           audio_file = audio_file,
                           )

if __name__=="__main__":
    app.run(host="127.0.0.1", port=8080)

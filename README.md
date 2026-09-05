# Dyslexia AI Helper
This project is a Flask web application designed to make text easier to read for people with dyslexia. It uses AI to simplify text, translate it into different languages, and convert it to speech.

## File: `app.py`

### Key Features:

- **Text Simplification**: Uses OpenAI to rewrite text with simpler vocabulary and shorter sentences.
- **Translation**: Translates simplified text into multiple languages.
- **Text-to-Speech**: Uses gTTS to generate audio from the simplified or translated text.
- **File Upload**: Allows users to upload text files for processing.
- **Accessibility Options**:
  - Font selection
  - Color-blind/high-contrast mode
  - Text-to-speech
- **Audio Download**: Allows generated audio to be downloaded.

### Technologies:

- Python
- Flask
- OpenAI API
- gTTS
- HTML/CSS
- python-dotenv

## How It Works

1. User enters text or uploads a text file.
2. The text is simplified using OpenAI.
3. The simplified text is translated if another language is selected.
4. The result is converted into speech using gTTS.
5. The user can read, listen to, or download the result.

## Project Status

This is a **prototype** and is still being developed. The main features work, but some language support, file handling, and accessibility features may not work perfectly yet.

## Future Improvements

- Improve language and translation support
- Add PDF/DOCX file support
- Improve error handling
- Add more accessibility options
- Improve text-to-speech controls
- Improve the overall UI

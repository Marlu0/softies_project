from gtts import gTTS
import emoji
import os
from playsound import playsound
import tempfile

def speak_text(text: str, lang: str = 'en'):  # Changed default to 'en'
    """
    Speak the given text aloud using Google Text-to-Speech.

    :param text: The text to speak.
    :param lang: Language code (default is 'en' for English).
    """
    text = emoji.demojize(text)
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        temp_path = fp.name
        tts.save(temp_path)
    playsound(temp_path)
    os.remove(temp_path)

def list_voices():
    """
    Print available languages for gTTS.
    """
    from gtts.lang import tts_langs
    langs = tts_langs()
    for code, name in langs.items():
        print(f"{code}: {name}")

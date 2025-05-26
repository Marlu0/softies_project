import pyttsx3

def speak_text(text: str, voice_index: int = 2, rate: int = 150, volume: float = 1.0):
    """
    Speak the given text aloud using the specified voice, rate, and volume.

    :param text: The text to speak.
    :param voice_index: Index of the voice to use (default is 0).
    :param rate: Speed of speech (default is 150).
    :param volume: Volume level from 0.0 to 1.0 (default is 1.0).
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    else:
        print(f"⚠️ Invalid voice index: {voice_index}. Using default voice.")

    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    engine.say(text)
    engine.runAndWait()

def list_voices():
    """
    Print available TTS voices with their index and language info.
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"{index}: {voice.name} ({voice.languages})")

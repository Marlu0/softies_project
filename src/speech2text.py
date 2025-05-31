import queue
import os
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

# Path to your downloaded Vosk model directory
VOICE_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "vosk-model-small-en-us-0.15")
SAMPLE_RATE = 16000

# Load the Vosk model once at import time
print("🔧 Loading Vosk model...")
vosk_model = Model(VOICE_MODEL_PATH)

def listen_for_input(prompt="🎙️ Speak now (say 'stop' to quit):"):
    """
    Listens to the microphone and returns the first complete transcribed phrase.
    If the user says 'stop', returns the string 'stop'.
    """
    recognizer = KaldiRecognizer(vosk_model, SAMPLE_RATE)
    recognizer.SetWords(True)

    audio_queue = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(f"⚠️ {status}", flush=True)
        audio_queue.put(bytes(indata))

    print(prompt)
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        try:
            while True:
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        return text
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user.")
            return "stop"

def listen_for_input_stream(prompt="🎙️ Speak now (say 'stop' to quit):"):
    import time
    recognizer = KaldiRecognizer(vosk_model, SAMPLE_RATE)
    recognizer.SetWords(True)

    audio_queue = queue.Queue()

    def callback(indata, frames, time_, status):
        if status:
            print(f"⚠️ {status}", flush=True)
        audio_queue.put(bytes(indata))

    print(prompt)
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        try:
            last_partial = ""
            last_speech_time = time.time()
            silence_timeout = 2.5  # seconds of silence before finalizing (increase for more time)
            while True:
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        yield text
                        break
                    last_speech_time = time.time()
                else:
                    partial = json.loads(recognizer.PartialResult())
                    partial_text = partial.get("partial", "")
                    if partial_text:
                        last_speech_time = time.time()
                    if partial_text != last_partial:
                        yield partial_text
                        last_partial = partial_text
                # Check for silence timeout
                if time.time() - last_speech_time > silence_timeout:
                    # Finalize whatever is in the buffer
                    final_result = json.loads(recognizer.FinalResult())
                    final_text = final_result.get("text", "").strip()
                    if final_text:
                        yield final_text
                    break
        except KeyboardInterrupt:
            yield "stop"

# Optional standalone mode for testing
if __name__ == "__main__":
    while True:
        transcript = listen_for_input()
        if transcript == "stop":
            print("👋 Goodbye!")
            break
        print(f"📝 You said: {transcript}")

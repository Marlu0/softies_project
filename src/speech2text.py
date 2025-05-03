import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

# Path to your downloaded Vosk model directory
MODEL_PATH = "models/vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000

def listen_for_input(prompt="🎙️ Speak now (say 'stop' to quit):"):
    """
    Listens to the microphone and returns the first complete transcribed phrase.
    If the user says 'stop', returns the string 'stop'.
    """
    print("🔧 Loading Vosk model...")
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
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

# Optional standalone mode for testing
if __name__ == "__main__":
    while True:
        transcript = listen_for_input()
        if transcript == "stop":
            print("👋 Goodbye!")
            break
        print(f"📝 You said: {transcript}")

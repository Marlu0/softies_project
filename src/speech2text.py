import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

# Path to your downloaded Vosk model directory
MODEL_PATH = "models/vosk-model-small-en-us-0.15"

# Sample rate for your microphone
SAMPLE_RATE = 16000

def main():
    print("🔧 Loading model...")
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    recognizer.SetWords(True)

    audio_queue = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(f"⚠️ {status}", flush=True)
        audio_queue.put(bytes(indata))

    print("🎙️ Starting microphone stream...")
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("✅ Ready to speak. Press Ctrl+C to stop.")
        try:
            while True:
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    if result.get("text"):
                        if(result['text'] == "stop"):
                            print("'stop' detected. Bye!")
                            break;   
                        
                        print(f"📝 Transcription: {result['text']}")
                else:
                    # Partial (real-time) results can be shown if needed
                    partial_result = json.loads(recognizer.PartialResult())
                    if partial_result.get("partial"):
                        print(f"🟡 Partial: {partial_result['partial']}", end="\r")
        except KeyboardInterrupt:
            print("\n👋 Stopped by user.")

if __name__ == "__main__":
    main()
import torch
import torchaudio
from transformers import pipeline, WhisperProcessor, WhisperForCTC

# Initialize the Whisper ASR model and processor
processor = WhisperProcessor.from_pretrained("facebook/whisper-large")
model = WhisperForCTC.from_pretrained("facebook/whisper-large")

# Initialize the translation pipeline
translator = pipeline("translation", model="Helsinki-NLP/opus-mt")

# Function to perform ASR and MT
def speech_to_english():
    try:
        # Set the device to "cuda" if available, else use "cpu"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = model.to(device)
        model.eval()

        # Use the default microphone as the audio source
        with torchaudio.open("default") as source:
            print("Please start speaking...")

            # Listen for audio
            waveform, sample_rate = source

            # Perform ASR to transcribe the audio
            inputs = processor(waveform, return_tensors="pt", sample_rate=sample_rate).input_values.to(device)
            with torch.no_grad():
                logits = model(input_values=inputs).logits
                predicted_ids = torch.argmax(logits, dim=-1)
                transcription = processor.batch_decode(predicted_ids)[0]

            print("ASR Result:", transcription)

            # Perform MT to translate the ASR result to English
            translated_text = translator(transcription, src="auto", tgt="en")

            return translated_text[0]["translation_text"]
    except Exception as e:
        return str(e)

# Example usage for live input
while True:
    english_text = speech_to_english()
    print("Translated English Text:", english_text)

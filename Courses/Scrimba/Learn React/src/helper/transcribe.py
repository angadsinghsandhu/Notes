import speech_recognition as sr
from pydub import AudioSegment

# Convert WebM to WAV
file_name = "audio/01_SP/02/wwl"
audio = AudioSegment.from_file(f"{file_name}.webm", format="webm")
audio.export(f"{file_name}.wav", format="wav")

# Initialize recognizer
recognizer = sr.Recognizer()

# Load audio file
with sr.AudioFile(f"{file_name}.wav") as source:
    audio_data = recognizer.record(source)

# Transcribe audio
text = recognizer.recognize_google(audio_data)

# Save the transcription to a text file
text_file_path = f"{file_name}.txt"
with open(text_file_path, "w", encoding="utf-8") as text_file:
    text_file.write(text)

print(f"Transcription saved to: {text_file_path}")

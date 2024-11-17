import os
from google.cloud import texttospeech
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'demo_service_acc.json'
client = texttospeech.TextToSpeechClient()

def TTS(text_block):
    # Synthesize speech
    synthesis_input = texttospeech.SynthesisInput(text=text_block)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name = "en-US-Studio-Q"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=['small-bluetooth-speaker-class-device'],
        speaking_rate=0.8,
        pitch=1
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Ensure that no file exists before creating the new one
    if os.path.exists("output.mp3"):
        os.remove("output.mp3")

    with open("output.mp3", "wb") as output:
        output.write(response.audio_content)
        # File is now written and closed after writing the content

    print("Playing Audio Story...")

    # Add a small delay to ensure file is completely written before using it
    time.sleep(0.5)  # 100ms delay should be sufficient, but can be adjusted if needed

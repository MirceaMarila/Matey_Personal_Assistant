from google.cloud import texttospeech

from core.settings import BASE_DIR


def text_to_mp3(text: str, audio_name):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.MALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open(f"{BASE_DIR}\\audio\\{audio_name}.mp3", "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{audio_name}.mp3"')

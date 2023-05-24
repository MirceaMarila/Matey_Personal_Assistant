from google.cloud import texttospeech


def text_to_wav(text: str):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.MALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # The response's audio_content is binary.
    with open("audio\\hello.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')


text = """Late at night, guards on the battlements of Denmark's Elsinore castle are met by Horatio, Prince Hamlet's friend from school. The guards describe a ghost they have seen that resembles Hamlet's father, the recently-deceased king. At that moment, the Ghost reappears, and the guards and Horatio decide to tell Hamlet.
Claudius, Hamlet's uncle, married Hamlet's recently-widowed mother, becoming the new King of Denmark. Hamlet continues to mourn for his father's death and laments his mother's lack of loyalty. When Hamlet hears of the Ghost from Horatio, he wants to see it for himself.
Elsewhere, the royal attendant Polonius says farewell to his son Laertes, who is departing for France. Laertes warns his sister, Ophelia, away from Hamlet and thinking too much of his attentions towards her. """

text_to_wav("hello")

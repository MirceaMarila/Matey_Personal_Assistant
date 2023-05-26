# Python program to translate
# speech to text and text to speech

import re
import time
import speech_recognition as sr
import pyttsx3

def free_speech_to_text():
# Initialize the recognizer
    r = sr.Recognizer()


    # Function to convert text to
    # speech
    def SpeakText(command):
        # Initialize the engine
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()


    # Loop infinitely for user to
    # speak

    while True:

        # Exception handling to handle
        # exceptions at the runtime
        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()

                print("Did you say ", MyText)
                SpeakText(MyText)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")


def paid_speech_to_text():
    # pip install pyaudio requests websockets
    import pyaudio
    import websockets
    import asyncio
    import base64
    import json

    auth_key = 'feff361f26e2458e9a233cd0c9292f8d'

    FRAMES_PER_BUFFER = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    p = pyaudio.PyAudio()

    # starts recording
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )

    # the AssemblyAI endpoint we're going to hit
    URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

    speech = [""]
    global time1
    time1 = time.time()

    async def send_receive():
        print(f'Connecting websocket to url ${URL}')
        async with websockets.connect(
                URL,
                extra_headers=(("Authorization", auth_key),),
                ping_interval=5,
                ping_timeout=20
        ) as _ws:
            await asyncio.sleep(0.1)
            print("Receiving SessionBegins ...")
            session_begins = await _ws.recv()
            print(session_begins)
            print("Sending messages ...")

            async def send():
                while True:
                    try:
                        data = stream.read(FRAMES_PER_BUFFER)
                        data = base64.b64encode(data).decode("utf-8")
                        json_data = json.dumps({"audio_data": str(data)})
                        await _ws.send(json_data)
                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, "Not a websocket 4008 error"
                    await asyncio.sleep(0.01)

                return True

            async def receive():

                global time1
                while True:
                    try:
                        result_str = await _ws.recv()

                        text = json.loads(result_str)['text']
                        text = re.sub('[^A-Za-z0-9]+', ' ', text.strip().lower())
                        time2 = time.time()

                        if text:
                            speech[-1] = text
                            time1 = time2

                        elif int(time2 - time1) >= 2 and speech[-1]:
                            speech.append("")

                        print(speech)

                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, "Not a websocket 4008 error"

            send_result, receive_result = await asyncio.gather(send(), receive())

    asyncio.run(send_receive())


# free_speech_to_text()
paid_speech_to_text()
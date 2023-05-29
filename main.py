import sys
import pyaudio
import websockets
import asyncio
import base64
import json
import re
import time
from core.utils import play_audio_and_plot_voice, play_audio
from core.sound_plotting import plot_voice
from multiprocessing import Process, Manager


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


async def send_receive(manager_dict):
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
                    ##############################################################
                    text = json.loads(result_str)['text']
                    text = re.sub('[^A-Za-z0-9]+', ' ', text.strip().lower())
                    time2 = time.time()

                    if manager_dict['listen']:
                        if text:
                            speech[-1] = text
                            time1 = time2

                        elif int(time2 - time1) >= 1 and speech[-1]:
                            if manager_dict['hidden']:
                                names = ["mate", "made", "matthew", "matt", "mattie"]
                                for name in names:
                                    if 'hey ' + name in speech[-1]:
                                        manager_dict['listen'] = False
                                        play_audio("start")
                                        manager_dict['hidden'] = False
                                        play_audio_and_plot_voice(manager_dict, "hello")
                                        break

                            else:
                                if 'thank you' in speech[-1]:
                                    manager_dict['listen'] = False
                                    play_audio_and_plot_voice(manager_dict, "welcome")
                                    play_audio("exit")

                                elif 'exit' in speech[-1]:
                                    manager_dict['listen'] = False
                                    play_audio_and_plot_voice(manager_dict, "rude")
                                    play_audio("exit")

                                elif 'shut down' in speech[-1]:
                                    manager_dict['listen'] = False
                                    play_audio_and_plot_voice(manager_dict, "shutdown")
                                    sys.exit()

                                else:
                                    play_audio("ping")

                            speech.append("")

                        print(speech)
                    ##############################################################

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())


def listen(manager_dict):
    asyncio.run(send_receive(manager_dict))


if __name__ == "__main__":
    manager = Manager()
    manager_dict = manager.dict()
    manager_dict['plot'] = None
    manager_dict['listen'] = True
    manager_dict['hidden'] = True

    listen_process = Process(target=listen, args=(manager_dict, ))
    listen_process.start()

    plot_process = Process(target=plot_voice, args=(manager_dict, ))
    plot_process.start()

    listen_process.join()
    plot_process.join()

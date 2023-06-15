import os
import time
from multiprocessing import Process, Manager

from core.settings import BASE_DIR
from core.sound_plotting import plot_voice
from core.speech_to_text import listen
from core.utils import check_internet, play_audio, play_audio_and_plot_voice, read_from_config_json

if __name__ == "__main__":

    if not os.path.isdir(BASE_DIR + "\\results"):
        os.mkdir(BASE_DIR + "\\results")

    if not os.path.isdir(BASE_DIR + "\\shortcuts"):
        os.mkdir(BASE_DIR + "\\shortcuts")

    if not os.path.isdir(BASE_DIR + "\\images"):
        os.mkdir(BASE_DIR + "\\images")

    if not os.path.isdir(BASE_DIR + "\\downloads"):
        os.mkdir(BASE_DIR + "\\downloads")

    manager = Manager()
    manager_dict = manager.dict()

    manager_dict['chatgpt_api_key'] = read_from_config_json('chatgpt_api_key')
    manager_dict['openweather_api_key'] = read_from_config_json('openweather_api_key')
    manager_dict['assemblyai_api_key'] = read_from_config_json('assemblyai_api_key')
    manager_dict['windows_user'] = read_from_config_json('windows_user')
    manager_dict['chrome_exe_path'] = read_from_config_json('chrome_exe_path')
    manager_dict['tick_in_seconds'] = read_from_config_json('tick_in_seconds')

    manager_dict['plot'] = None
    manager_dict['listen'] = True
    manager_dict['hidden'] = True
    manager_dict['loading'] = False
    manager_dict['shut_down'] = False
    manager_dict['title'] = False
    manager_dict['suptitle'] = False
    time1 = time.time()

    if not check_internet():
        plot_process = Process(target=plot_voice, args=(manager_dict,))
        plot_process.start()
        play_audio("start")
        manager_dict['hidden'] = False
        play_audio_and_plot_voice(manager_dict, "no_internet")
        manager_dict['shut_down'] = True
        plot_process.join()
        play_audio("exit")

    else:
        listen_process = Process(target=listen, args=(manager_dict, time1))
        listen_process.start()

        plot_process = Process(target=plot_voice, args=(manager_dict, ))
        plot_process.start()

        listen_process.join()
        plot_process.join()

        if manager_dict['shut_down']:
            play_audio("exit")

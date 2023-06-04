import time
from core.sound_plotting import plot_voice
from multiprocessing import Process, Manager
from core.speech_to_text import listen
from core.utils import check_internet, play_audio, play_audio_and_plot_voice, initialize_winsound


if __name__ == "__main__":
    manager = Manager()
    manager_dict = manager.dict()
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

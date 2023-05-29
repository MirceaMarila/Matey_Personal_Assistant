import time
from core.sound_plotting import plot_voice
from multiprocessing import Process, Manager
from core.speech_to_text import listen


if __name__ == "__main__":
    manager = Manager()
    manager_dict = manager.dict()
    manager_dict['plot'] = None
    manager_dict['listen'] = True
    manager_dict['hidden'] = True
    time1 = time.time()

    listen_process = Process(target=listen, args=(manager_dict, time1))
    listen_process.start()

    plot_process = Process(target=plot_voice, args=(manager_dict, ))
    plot_process.start()

    listen_process.join()
    plot_process.join()

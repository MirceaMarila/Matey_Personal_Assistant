from playsound import playsound
from core.settings import BASE_DIR
import threading
from core.sound_plotting import plot_voice
import win32gui
import time
import pythoncom
import win32com.client


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def play_audio(name, manager_dict=None, semaphore=None):
    if semaphore:
        # semaphore.acquire()
        manager_dict['semaphore'] = True
        while manager_dict['semaphore'] is True:
            pass

    while True:
        try:
            playsound(BASE_DIR + f"\\audio\\{name}.mp3")
            break

        except:
            pass


def play_audio_and_plot_voice(manager_dict, name):
    # semaphore = threading.Semaphore()
    thread = threading.Thread(target=play_audio, args=(name, manager_dict, True))
    thread.start()
    # plot_voice(name, extention, semaphore)
    manager_dict['plot'] = name
    thread.join()

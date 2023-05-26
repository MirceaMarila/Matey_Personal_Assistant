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


def play_audio(name, extention="mp3", semaphore=None):
    if semaphore:
        semaphore.acquire()

    while True:
        try:
            playsound(BASE_DIR + f"\\audio\\{name}.{extention}")
            break
        except:
            pass


def play_audio_and_plot_voice(name, extention="mp3"):
    semaphore = threading.Semaphore()
    thread = threading.Thread(target=play_audio, args=(name, extention, semaphore))
    thread.start()
    plot_voice(name, extention, semaphore)

import datetime
import os.path
from playsound import playsound
from core.settings import BASE_DIR
import threading
from core.sound_plotting import plot_voice
import win32gui
import time
import pythoncom
from core.handle_tasks import chat_gpt
from core.text_to_speech import text_to_mp3
from urllib import request
from os import listdir
from os.path import isfile, join
import difflib


def check_internet():
    try:
        request.urlopen('http://google.com', timeout=1)
        return True

    except:
        return False


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def play_audio(name, manager_dict=None, semaphore=None):
    if semaphore:
        manager_dict['semaphore'] = True
        while manager_dict['semaphore'] is True:
            pass

    if name != 'loading':
        while True:
            try:
                playsound(BASE_DIR + f"\\audio\\{name}.mp3")
                break

            except:
                pass


def play_audio_and_plot_voice(manager_dict, name):
    thread = threading.Thread(target=play_audio, args=(name, manager_dict, True))
    thread.start()
    manager_dict['plot'] = name
    thread.join()


def process_task(manager_dict, task):
    if 'search' in task:
        if ' and save the result' in task:
            if check_internet():

                manager_dict['loading'] = True
                question = task.split('search')[-1].split(' and save the result')[0]
                result = chat_gpt(task).strip()
                manager_dict['loading'] = False

                today = datetime.datetime.now().strftime("%d_%m_%Y")
                filepath = BASE_DIR + f"\\results\\search_results_{today}.txt"

                if os.path.isfile(filepath):
                    with open(filepath, "r") as file:
                        text = file.read()

                    text += f"Q: {question}\nA: {result}\n\n"

                    with open(filepath, "w") as file:
                        file.write(text)

                else:
                    with open(filepath, "w") as file:
                        file.write(f"Q: {task}\nA: {result}\n\n")

                play_audio_and_plot_voice(manager_dict, "result_saved")

            else:
                play_audio_and_plot_voice(manager_dict, "no_internet")

        else:
            if check_internet():
                manager_dict['loading'] = True
                result = chat_gpt(task)
                manager_dict['loading'] = False
                text_to_mp3(result, "chat_gpt")
                play_audio_and_plot_voice(manager_dict, "chat_gpt")

            else:
                play_audio_and_plot_voice(manager_dict, "no_internet")

    elif 'open' in task:
        manager_dict['loading'] = True
        program = task.split('open ')[-1]
        shortcuts_folder = BASE_DIR + "\\shortcuts"
        shortcuts = [f for f in listdir(shortcuts_folder) if isfile(join(shortcuts_folder, f))]

        cutoff = 1.0
        open_program = difflib.get_close_matches(program, shortcuts, 1, cutoff)
        while not open_program and cutoff >= 0.5:
            cutoff -= 0.1
            open_program = difflib.get_close_matches(program, shortcuts, 1, cutoff)

        manager_dict['loading'] = False
        if not open_program:
            play_audio_and_plot_voice(manager_dict, "app_not_found")

        else:
            play_audio_and_plot_voice(manager_dict, "ok")
            manager_dict['hidden'] = True
            os.startfile(shortcuts_folder + f"\\{open_program[0]}")

    else:
        play_audio_and_plot_voice(manager_dict, "didnt_understand")

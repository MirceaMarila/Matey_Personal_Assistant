import datetime
from os import listdir
from os.path import isfile, join
from core.settings import BASE_DIR
from core.text_to_speech import text_to_mp3
from core.utils import play_audio_and_plot_voice, chat_gpt, get_weather, get_current_city, save_results, \
    get_closest_match, play_audio, open_close_app, play_a_random_song, play_on_youtube, download_from_youtube, \
    translate_text_and_save_mp3, where_am_i, open_camera_to_take_a_picture
from multiprocessing import Process
import threading
import screen_brightness_control as sbc
from pynput.keyboard import Key, Controller
import time
from word2number import w2n
import os
import sys


def process_task(manager_dict, task):
    try:
        if 'search' in task or 'tell me a joke' in task:
            manager_dict['loading'] = True
            result = chat_gpt(task.split('search ')[-1].strip() if 'search' in task else task).strip()
            text_to_mp3(result, "temp")
            manager_dict['loading'] = False

            if 'tell me a joke' in task:
                manager_dict['suptitle'] = False

            play_audio_and_plot_voice(manager_dict, "temp", result)
            save_results(task, result.replace('\n', ' '), 'search')

        elif 'how is the weather' in task:
            manager_dict['loading'] = True
            if 'weather in' in task:
                city = task.split('weather in')[-1].strip()
                weather = get_weather(city)
                manager_dict['loading'] = False

                if weather:
                    text_to_mp3(weather, "temp")
                    play_audio_and_plot_voice(manager_dict, "temp", weather)
                    save_results(task, weather, "weather")
                else:
                    play_audio_and_plot_voice(manager_dict, "no_weather")

            else:
                city = get_current_city()
                if not city:
                    manager_dict['loading'] = False
                    play_audio_and_plot_voice(manager_dict, "no_city")

                else:
                    weather = get_weather(city)
                    manager_dict['loading'] = False

                    if weather:
                        text_to_mp3(weather, "temp")
                        play_audio_and_plot_voice(manager_dict, "temp", weather)
                        save_results(task, weather, "weather")
                    else:
                        play_audio_and_plot_voice(manager_dict, "no_weather")

        elif 'open camera' in task:
            play_audio_and_plot_voice(manager_dict, "camera")
            manager_dict['loading'] = True
            camera_process = Process(target=open_camera_to_take_a_picture)
            camera_process.start()
            camera_process.join()
            manager_dict['loading'] = False
            manager_dict['title'] = "Picture saved in the images folder!"
            play_audio_and_plot_voice(manager_dict, "picture_saved")

        elif 'open' in task:
            manager_dict['loading'] = True
            program = task.split('open ')[-1].strip() + ".exe - Shortcut.lnk"
            shortcuts_folder = BASE_DIR + "\\shortcuts"
            shortcuts = [f for f in listdir(shortcuts_folder) if isfile(join(shortcuts_folder, f))]
            open_program = get_closest_match(word=program, words_list=shortcuts, cutoff_min=0.5)

            manager_dict['loading'] = False
            if not open_program:
                play_audio_and_plot_voice(manager_dict, "app_not_found")

            else:
                text = f"Opening {open_program[0].split(' - ')[0].split('.exe')[0]}"
                text_to_mp3(text, "temp")
                play_audio_and_plot_voice(manager_dict, "temp", text)
                open_close_app(shortcuts_folder + f"\\{open_program[0]}", "open")

        elif 'close' in task:
            manager_dict['loading'] = True
            program = task.split('close ')[-1].strip() + ".exe - Shortcut.lnk"
            shortcuts_folder = BASE_DIR + "\\shortcuts"
            shortcuts = [f for f in listdir(shortcuts_folder) if isfile(join(shortcuts_folder, f))]
            close_program = get_closest_match(word=program, words_list=shortcuts, cutoff_min=0.5)

            if not close_program:
                manager_dict['loading'] = False
                play_audio_and_plot_voice(manager_dict, "app_not_found")

            else:
                short_name = close_program[0].split(' - ')[0].split('.exe')[0]
                closed = open_close_app(close_program[0].split(' - ')[0], 'close')
                manager_dict['loading'] = False

                if closed:
                    text = f"{short_name} closed"
                    text_to_mp3(text, "temp")
                    play_audio_and_plot_voice(manager_dict, "temp", text)

                else:
                    text = f"{short_name} is not opened!"
                    text_to_mp3(text, "temp")
                    manager_dict['loading'] = False
                    play_audio_and_plot_voice(manager_dict, "temp", text)

        elif 'random song' in task:
            play_audio_and_plot_voice(manager_dict, "ok")
            play_process = Process(target=play_a_random_song, args=(manager_dict,))
            play_process.start()
            play_process.join()
            manager_dict['loading'] = False
            play_audio_and_plot_voice(manager_dict, "back_in_business")

        elif 'play' in task:
            song = task.split('play ')[-1]
            play_audio_and_plot_voice(manager_dict, "ok")
            play_process = Process(target=play_on_youtube, args=(manager_dict, song))
            play_process.start()
            play_process.join()
            manager_dict['loading'] = False
            play_audio_and_plot_voice(manager_dict, "back_in_business")

        elif 'download' in task:
            song = task.split('download ')[-1]
            text = f"Ok! Downloading {song}"
            text_to_mp3(text, "temp")
            play_audio_and_plot_voice(manager_dict, "temp", text)
            downloaded = [False]

            try:
                play_process = Process(target=download_from_youtube, args=(manager_dict, song, downloaded))
                play_process.start()
                play_process.join()

            except:
                pass

            finally:
                manager_dict['loading'] = False
                if downloaded[0]:
                    play_audio_and_plot_voice(manager_dict, "download")
                else:
                    play_audio_and_plot_voice(manager_dict, "try_again")

        elif 'set brightness to' in task or 'set the brightness to' in task:
            brightness = w2n.word_to_num(task.split('set brightness to ')[-1].strip())
            sbc.set_brightness(brightness)
            text = f"Brightness set to {brightness}%"
            text_to_mp3(text, "temp")
            play_audio_and_plot_voice(manager_dict, "temp", text)

        elif 'increase volume' in task or 'increased volume' in task or 'increase the volume' in task:
            units = w2n.word_to_num(task.split('increase volume by ')[-1].strip())
            keyboard = Controller()

            for i in range(int(units/2)):
                keyboard.press(Key.media_volume_up)
                keyboard.release(Key.media_volume_up)
                time.sleep(0.1)

            text = f"Increased volume by {units} units"
            text_to_mp3(text, "temp")
            play_audio_and_plot_voice(manager_dict, "temp", text)

        elif 'decrease volume' in task or 'decreased volume' in task or 'decrease the volume' in task:
            units = w2n.word_to_num(task.split('decrease volume by ')[-1].strip())
            keyboard = Controller()

            for i in range(int(units/2)):
                keyboard.press(Key.media_volume_down)
                keyboard.release(Key.media_volume_down)
                time.sleep(0.1)

            text = f"Decreased volume by {units} units"
            text_to_mp3(text, "temp")
            play_audio_and_plot_voice(manager_dict, "temp", text)

        elif 'unmute volume' in task:
            keyboard = Controller()
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)
            play_audio_and_plot_voice(manager_dict, "volume_unmuted")

        elif 'mute volume' in task:
            keyboard = Controller()
            keyboard.press(Key.media_volume_mute)
            keyboard.release(Key.media_volume_mute)
            play_audio_and_plot_voice(manager_dict, "volume_muted")

        elif 'translate' in task:
            manager_dict['loading'] = True
            to_language = task.split('translate in ')[-1].split(' ')[0]
            text = task.strip().split(f'{to_language} ')[-1]
            result = [False]
            thread = threading.Thread(target=translate_text_and_save_mp3, args=(text, to_language, result))
            thread.start()
            thread.join()
            manager_dict['loading'] = False

            if result[0]:
                play_audio_and_plot_voice(manager_dict, "temp", result[0])
                save_results(task, result[0].replace('\n', ' '), 'translate')

            else:
                play_audio_and_plot_voice(manager_dict, "try_again")

        elif 'translating' in task:
            manager_dict['loading'] = True
            to_language = task.split('translating ')[-1].split(' ')[0]
            text = task.strip().split(f'{to_language} ')[-1]
            result = [False]
            thread = threading.Thread(target=translate_text_and_save_mp3, args=(text, to_language, result))
            thread.start()
            thread.join()
            manager_dict['loading'] = False

            if result[0]:
                play_audio_and_plot_voice(manager_dict, "temp", result[0])
                save_results(task, result[0].replace('\n', ' '), 'translate')

        elif 'where am i' in task:
            manager_dict['loading'] = True
            location = where_am_i()
            manager_dict['loading'] = False

            if location:
                play_audio_and_plot_voice(manager_dict, "temp", location)
                save_results(task, location.replace('\n', ' '), 'location')

            else:
                play_audio_and_plot_voice(manager_dict, "try_again")

        elif 'your name' in task:
            play_audio_and_plot_voice(manager_dict, "name")

        elif 'old are you' in task:
            then = datetime.datetime(2023, 6, 18)
            now = datetime.datetime.now()
            duration = now - then
            days = str(duration.days)
            text = f"I am {days} days old!"
            text_to_mp3(text, "temp")
            play_audio_and_plot_voice(manager_dict, "temp", text)

        elif 'your gender' in task:
            play_audio_and_plot_voice(manager_dict, "gender")

        elif 'think about cortana' in task:
            play_audio_and_plot_voice(manager_dict, "cortana")
        # elif 'walrus' in task:
        #     play_audio_and_plot_voice(manager_dict, "walrus")

        else:
            play_audio_and_plot_voice(manager_dict, "didnt_understand")

    except Exception as e:
        print(e)
        manager_dict['hidden'] = False
        manager_dict['loading'] = False
        play_audio_and_plot_voice(manager_dict, "try_again")


# process_task(None, "play a random song")

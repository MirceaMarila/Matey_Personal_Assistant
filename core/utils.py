import time
import keyboard
import openai
from playsound import playsound
import threading
from urllib import request
import geocoder
from geopy.geocoders import Nominatim
import requests
import datetime
import difflib
import psutil
import io
import soundfile
from os import listdir
from os.path import isfile, join
import os
from core.settings import USER
import winsound
from core.sound_plotting import load_song
from core.text_to_speech import text_to_mp3
from core.web_driver import ChromeDriver, ElementFinder
from core.web_elements import Button, GenericElement, TextBox
import speech_recognition as spr
import googletrans
from googletrans import Translator
from gtts import gTTS
from core.settings import BASE_DIR
import cv2


def check_internet():
    timeout = 5
    flag = False

    while not flag and timeout:
        try:
            request.urlopen('http://google.com', timeout=1)
            flag = True

        except:
            time.sleep(.5)
            timeout -= 0.5

    return flag


def play_audio(name, manager_dict=None, semaphore=None):
    if semaphore:
        manager_dict['semaphore'] = True
        while manager_dict['semaphore'] is True:
            pass

    if name != 'loading':
        if name != 'temp':
            playsound(BASE_DIR + f"\\audio\\{name}.mp3")

        else:
            voice1, sample_rate = load_song(f"{BASE_DIR}\\audio\\temp.mp3")
            virtual_file = io.BytesIO()
            soundfile.write(virtual_file, voice1, int(sample_rate), format="WAV")
            virtual_file.seek(0)
            winsound.PlaySound(virtual_file.read(), winsound.SND_MEMORY)
            virtual_file.close()


def play_audio_and_plot_voice(manager_dict, name, text=None):
    thread = threading.Thread(target=play_audio, args=(name, manager_dict, True))
    thread.start()
    manager_dict['plot'] = name
    if text:
        manager_dict['title'] = text
    thread.join()


def get_current_city(country=False):
    g = geocoder.ip('me')
    coord = dict()

    coord['Latitude'] = g.latlng[0]
    coord['Longitude'] = g.latlng[1]

    geolocator = Nominatim(user_agent="geoapiExercises")
    coord = f"{coord['Latitude']}, {coord['Longitude']}"

    location = geolocator.reverse(coord, exactly_one=True)
    address = location.raw['address']

    if not country:
        village = address.get('city', '')
        city = address.get('city', '')
        county = address.get('county', '')

        return city if city else village if village else county

    else:
        return address.get('country', '')


def get_weather(city):
    api = "ff8ed9c3bfec39e852053c57df5dbd86"
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, api)

    weather = False
    try:
        res = requests.get(url)
        data = res.json()

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = round(float(data['wind']['speed']) * 3.6, 1)
        description = data['weather'][0]['description']
        temp = round(float(data['main']['temp']) - 273.15, 1)

        weather = f"Temperature: {temp} °C, Wind: {wind} km/h, Pressure: {pressure} mb, " \
                  f"Humidity: {humidity} %, Description: {description}"

    except:
        pass

    finally:
        return weather


def chat_gpt(search_text):
    openai.api_key = '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'
    model_engine = "text-davinci-003"
    prompt = search_text + ". give me just the result"

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    return response


def save_results(question, answer, file_name):
    today = datetime.datetime.now().strftime("%d_%m_%Y")
    folder = BASE_DIR + f"\\results\\{today}"

    if file_name == 'weather':
        encoding = "windows-1252"
    else:
        encoding = "utf-8"

    if not os.path.isdir(folder):
        os.mkdir(folder)

    filepath = BASE_DIR + f"\\results\\{today}\\{file_name}_results.txt"
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding=encoding) as file:
            text = file.read()

        text += f"Q: {question}\nA: {answer}\n\n"

        with open(filepath, "w", encoding=encoding) as file:
            file.write(text)

    else:
        with open(filepath, "w", encoding=encoding) as file:
            file.write(f"Q: {question}\nA: {answer}\n\n")


def get_closest_match(word, words_list, cutoff_min):
    cutoff = 1.0
    program = difflib.get_close_matches(word, words_list, 1, cutoff)
    while not program and cutoff >= cutoff_min:
        cutoff -= 0.1
        program = difflib.get_close_matches(word, words_list, 1, cutoff)

    return program


def open_close_app(path, open_close):

    def open_close_thread(path, open_close, closed):
        if open_close == 'open':
            os.startfile(path)

        else:
            for p in psutil.process_iter():
                if path in p.name():
                    p.kill()
                    p.terminate()
                    closed[0] = True

            return closed

    closed = [False]
    thread = threading.Thread(target=open_close_thread, args=(path, open_close, closed))
    thread.start()
    thread.join()

    return closed[0]


def initialize_winsound():
    voice1, sample_rate = load_song(f"{BASE_DIR}\\audio\\silence.mp3")
    virtual_file = io.BytesIO()
    soundfile.write(virtual_file, voice1, int(sample_rate), format="WAV")
    virtual_file.seek(0)
    winsound.PlaySound(virtual_file.read(), winsound.SND_MEMORY)
    virtual_file.close()


def wait_for_key_pressed_or_time_expired(music_time, driver):
    class KeyEventThread(threading.Thread):
        def run(self):
            timeout = 3
            while timeout and datetime.datetime.now() < music_time:
                try:
                    url = driver.current_url
                    if keyboard.is_pressed('ctrl'):
                        timeout -= 1
                        time.sleep(1)

                    elif timeout < 3:
                        timeout += 1

                except:
                    break

    kethread = KeyEventThread()
    kethread.start()
    kethread.join()
    play_audio("ping")

    if driver:
        try:
            driver.close()
            driver.quit()
        except:
            pass


def play_a_random_song(manager_dict):
    manager_dict['listen'] = False
    manager_dict['loading'] = True
    driver = ChromeDriver(options=['--incognito'])
    finder = ElementFinder(driver)

    driver.get("https://www.chosic.com/random-songs-generator-with-links-to-spotify-and-youtube/")
    driver.maximize_window()

    Button(driver, finder, xpath="//button/span[text()=\"AGREE\"]").click()
    Button(driver, finder, xpath="//button[text()=\"Generate\"]").click()

    finder.invisibility_of_element_located(['xpath', "//div[@class=\"main-loading\"]"])
    time.sleep(1)

    iframe = GenericElement(driver, finder, xpath="//iframe[@id=\"featured-video\"]", clickable=False)
    title = iframe.element.get_attribute('title')
    text_to_mp3(f"Playing {title}. Hold control for 3 seconds to stop the song.", "temp")

    duration = chat_gpt(f"what is the lenght of \"{title}\" song")
    try:
        seconds = int(duration.split(' minutes')[0]) * 60 + (
            0 if 'seconds' not in duration else int(duration.split(' seconds')[0].split('and ')[-1]))
    except:
        seconds = 180

    manager_dict['loading'] = False
    play_audio_and_plot_voice(manager_dict, "temp")
    manager_dict['hidden'] = True

    iframe.click()
    finish_time = datetime.datetime.now() + datetime.timedelta(0, seconds)
    wait_for_key_pressed_or_time_expired(finish_time, driver)
    manager_dict['listen'] = True
    play_audio("start")
    manager_dict['hidden'] = False


def play_on_youtube(manager_dict, song):
    manager_dict['listen'] = False
    manager_dict['loading'] = True
    driver = ChromeDriver(options=['--incognito'])
    finder = ElementFinder(driver)

    driver.get("https://www.youtube.com/")
    driver.maximize_window()

    GenericElement(driver, finder, "(//tp-yt-paper-dialog//div[@class=\"yt-spec-touch-feedback-shape__stroke\"])[4]", clickable=False).click()
    time.sleep(1)
    TextBox(driver, finder, xpath="//input[@id=\"search\"]").write_text(song)
    Button(driver, finder, xpath="//button[@id=\"search-icon-legacy\"]").click()

    text_to_mp3(f"Playing {song}. Some youtube ads might appear. Hold control for 3 seconds to stop the song.", "temp")
    duration = chat_gpt(f"what is the lenght of \"{song}\" song")
    try:
        seconds = int(duration.split(' minutes')[0]) * 60 + 1 + (
            0 if 'seconds' not in duration else int(duration.split(' seconds')[0].split('and ')[-1]))
    except:
        seconds = 240

    manager_dict['loading'] = False
    play_audio_and_plot_voice(manager_dict, "temp")
    manager_dict['hidden'] = True

    Button(driver, finder, xpath="(//ytd-video-renderer//a)[1]").click()
    finish_time = datetime.datetime.now() + datetime.timedelta(0, seconds)
    wait_for_key_pressed_or_time_expired(finish_time, driver)

    manager_dict['listen'] = True
    play_audio("start")
    manager_dict['hidden'] = False


def download_from_youtube(manager_dict, song):
    manager_dict['loading'] = True
    manager_dict['listen'] = False
    driver = ChromeDriver(options=['--incognito'])
    finder = ElementFinder(driver)

    driver.get("https://www.youtube.com/")
    driver.maximize_window()

    GenericElement(driver, finder, "(//tp-yt-paper-dialog//div[@class=\"yt-spec-touch-feedback-shape__stroke\"])[4]", clickable=False).click()
    time.sleep(1)

    TextBox(driver, finder, xpath="//input[@id=\"search\"]").write_text(song)
    Button(driver, finder, xpath="//button[@id=\"search-icon-legacy\"]").click()
    Button(driver, finder, xpath="(//ytd-video-renderer//a)[1]").click()

    url = driver.current_url
    driver.get("https://ytmp3.nu/d06/")
    TextBox(driver, finder, xpath="//input[@type=\"text\"]").write_text(url)
    Button(driver, finder, xpath="//input[@type=\"submit\"]").click()

    Button(driver, finder, xpath="//a[@class=\"button\"][contains(text(), \"Download\")]").click()
    path = fr"C:\Users\{USER}\Downloads"
    download_wait(path)

    driver.close()
    driver.quit()

    downloads_files = [f for f in listdir(path) if isfile(join(path, f))]
    file_name = get_closest_match(song, downloads_files, cutoff_min=0.3)[0]
    os.rename(fr"{path}\{file_name}", f"{BASE_DIR}\\downloads\\{file_name}")

    manager_dict['loading'] = False
    manager_dict['listen'] = True


def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 30:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1


def translate_text_and_save_mp3(text, to_lang, result):
    # getting the right language to translate text into
    languages_dict = dict(googletrans.LANGUAGES)
    closest_language = get_closest_match(to_lang, languages_dict.values(), cutoff_min=0.5)[0]
    to_lang = list(languages_dict.keys())[list(languages_dict.values()).index(closest_language)]

    # Translator method for translation
    translator = Translator()

    # short form of english in which
    # you will speak
    from_lang = 'en'

    # Using try and except block to improve
    # its efficiency.
    try:

        # Using translate() method which requires
        # three arguments, 1st the sentence which
        # needs to be translated 2nd source language
        # and 3rd to which we need to translate in
        text_to_translate = translator.translate(text,
                                                 src=from_lang,
                                                 dest=to_lang)

        # Storing the translated text in text
        # variable
        text = text_to_translate.text

        # Using Google-Text-to-Speech ie, gTTS() method
        # to speak the translated text into the
        # destination language which is stored in to_lang.
        # Also, we have given 3rd argument as False because
        # by default it speaks very slowly
        speak = gTTS(text=text, lang=to_lang, slow=False)

        # Using save() method to save the translated
        # speech in capture_voice.mp3
        speak.save(BASE_DIR + "\\audio\\temp.mp3")

        result[0] = text

    # Here we are using except block for UnknownValue
    # and Request Error and printing the same to
    # provide better service to the user.
    except spr.UnknownValueError:
        print("Unable to Understand the Input")
        result[0] = False

    except spr.RequestError as e:
        print("Unable to provide Required Output".format(e))
        result[0] = False


def where_am_i():
    try:
        country = get_current_city(country=True)
        city = get_current_city()
        text = f"{city}, {country}"
        languages_dict = dict(googletrans.LANGUAGES)
        closest_language = get_closest_match(country, languages_dict.values(), cutoff_min=0.3)[0]
        to_lang = list(languages_dict.keys())[list(languages_dict.values()).index(closest_language)]
        speak = gTTS(text=text, lang=to_lang, slow=False)
        speak.save(BASE_DIR + "\\audio\\temp.mp3")
        return text

    except:
        return False


def open_camera_to_take_a_picture():
    webcam = cv2.VideoCapture(0)
    time.sleep(2)
    while True:

        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)

            if key == ord('s'):
                today = datetime.datetime.now().strftime("%d_%m_%Y")
                folder = BASE_DIR + f"\\images\\{today}"
                timestamp = datetime.datetime.now().strftime("%H_%M_%S")

                if not os.path.isdir(folder):
                    os.mkdir(folder)

                path = f"{BASE_DIR}\\images\\{today}\\saved_img_{timestamp}.jpg"
                cv2.imwrite(path, frame)
                webcam.release()

                img_ = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
                cv2.imwrite(path, img_)
                break

            elif key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break

        except KeyboardInterrupt:
            webcam.release()
            cv2.destroyAllWindows()
            break

        except:
            break


# md = dict()
# download_from_youtube(md, "metallica enter sandman")
# translate_text_and_save_mp3("text", "romanian")
# print(get_current_city())
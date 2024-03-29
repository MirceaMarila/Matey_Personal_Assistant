import librosa
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pylab
from PIL import Image

from core.settings import BASE_DIR


def load_song(song_path):
    y = librosa.load(song_path)
    data = y[0]
    sample_rate = y[1]

    return np.array(data), sample_rate


def plot_voice_frame(y, manager_dict):
    img_path = f"{BASE_DIR}\\images\\sphere.png"
    img = Image.open(img_path)
    width = img.width
    height = img.height

    mpl.rcParams['toolbar'] = 'None'
    plt.axis('off')

    x = np.linspace(0, len(y), len(y))
    img = plt.imread(img_path)
    plt.imshow(img, extent=[0, width, -height/2, height/2])
    params = {"text.color": "white"}
    plt.rcParams.update(params)

    if manager_dict['suptitle'] and 'hey' not in manager_dict['suptitle']:
        plt.suptitle("You: " + manager_dict['suptitle'])

    if manager_dict['title']:
        plt.title("Matey: " + manager_dict['title'])

    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Matey')
    fig.patch.set_facecolor('black')

    plt.plot(x/4.4+120, y*50-20, color="white")
    plt.ylim(-height/2, height/2)
    plt.xlim(0, width)


def plot_and_show_voice(manager_dict, semaphore, voice, sample_rate, nr_of_seconds, tick_samples, tick_in_seconds):

    for i, j in zip(range(0, int(sample_rate * nr_of_seconds), tick_samples),
                    range(tick_samples, int(sample_rate * nr_of_seconds), tick_samples)):
        aux = voice[i:j]
        plot_voice_frame(aux, manager_dict)

        if semaphore and manager_dict['semaphore']:
            manager_dict['semaphore'] = False

        plt.draw()
        plt.pause(tick_in_seconds / 2)
        plt.clf()


def interractive_plot_draw(manager_dict, semaphore, audio_name):
    plt.ion()
    voice_path = f"{BASE_DIR}\\audio\\{audio_name}.mp3"

    voice, sample_rate = load_song(voice_path)
    nr_of_seconds = len(voice) / sample_rate
    tick_in_seconds = manager_dict['tick_in_seconds']

    tick_samples = int(sample_rate * tick_in_seconds)
    plot_and_show_voice(manager_dict, semaphore, voice, sample_rate, nr_of_seconds, tick_samples, tick_in_seconds)


def plot_voice(manager_dict):

    while True:
        if manager_dict['shut_down']:
            if plt.get_fignums():
                plt.close()
            return

        try:
            if manager_dict['plot']:

                voice_name = manager_dict['plot']
                interractive_plot_draw(manager_dict, True, voice_name)

                manager_dict['listen'] = True
                manager_dict['plot'] = None

                if voice_name in ['welcome', 'rude'] and plt.get_fignums():
                    plt.close()
                    manager_dict['hidden'] = True

                else:
                    manager_dict['hidden'] = False

            elif not manager_dict['hidden']:

                if not manager_dict['loading']:
                    interractive_plot_draw(manager_dict, False, 'silence')

                else:
                    interractive_plot_draw(manager_dict, False, 'loading')

            else:
                if plt.get_fignums():
                    plt.close()

        except:
            pass

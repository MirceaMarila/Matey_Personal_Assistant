import pylab
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import librosa
import timeit
import random
from multiprocessing import Pool
from tqdm import tqdm
import os
import matplotlib as mpl
from core.settings import BASE_DIR


def load_song(song_path):
    y = librosa.load(song_path)
    data = y[0]
    sample_rate = y[1]

    return np.array(data), sample_rate


def plot_voice_frame(y):
    img_path = f"{BASE_DIR}\\images\\sphere.png"
    img = Image.open(img_path)
    width = img.width
    height = img.height

    mpl.rcParams['toolbar'] = 'None'
    plt.axis('off')

    x = np.linspace(0, len(y), len(y))
    img = plt.imread(img_path)
    plt.imshow(img, extent=[0, width, -height/2, height/2])

    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Matey')
    fig.patch.set_facecolor('black')

    plt.plot(x, y*50, color="white")
    plt.ylim(-height/2, height/2)
    plt.xlim(0, width)


def plot_and_show_voice(semaphore, voice, sample_rate, nr_of_seconds, tick_samples, tick_in_seconds):
    used_semaphore = False
    for i, j in zip(range(0, int(sample_rate * nr_of_seconds), tick_samples),
                    range(tick_samples, int(sample_rate * nr_of_seconds), tick_samples)):
        aux = voice[i:j]
        plot_voice_frame(aux)
        if semaphore and not used_semaphore:
            semaphore.release()
            used_semaphore = True
        plt.draw()
        plt.pause(tick_in_seconds / 2)
        plt.clf()
    plt.close()


def plot_voice(manager_dict, semaphore=None):
    while True:
        if manager_dict['plot'] != "nothing":
            voice_name = manager_dict['plot']
            plt.ion()
            voice_path = f"{BASE_DIR}\\audio\\{voice_name}.mp3"

            voice, sample_rate = load_song(voice_path)
            nr_of_seconds = len(voice) / sample_rate
            tick_in_seconds = 0.05

            tick_samples = int(sample_rate * tick_in_seconds)
            # plot_and_show_voice(semaphore, voice, sample_rate, nr_of_seconds, tick_samples, tick_in_seconds)
            used_semaphore = False
            for i, j in zip(range(0, int(sample_rate * nr_of_seconds), tick_samples),
                            range(tick_samples, int(sample_rate * nr_of_seconds), tick_samples)):
                aux = voice[i:j]
                plot_voice_frame(aux)

                if semaphore and not used_semaphore:
                    semaphore.release()
                    used_semaphore = True

                plt.draw()
                plt.pause(tick_in_seconds / 2)
                plt.clf()

            else:
                plt.close()


if __name__ == '__main__':
    # get_best_tick()
    # print(timeit.timeit(plot_voice, number=1))
    plot_voice("silence")

import os

import matplotlib.pyplot as plt
import numpy as np
import librosa
import timeit
import random
from multiprocessing import Pool
from tqdm import tqdm


def load_song(song_path):
    y = librosa.load(song_path)
    data = y[0]
    sample_rate = y[1]

    return np.array(data), sample_rate


def plot_voice_frame(y):
    x = np.linspace(0, len(y), len(y))

    plt.plot(x, y)
    plt.ylim((-3, 3))


def plot_and_show_voice(voice, sample_rate, nr_of_seconds, tick_samples, tick_in_seconds):
    for i, j in zip(range(0, int(sample_rate * nr_of_seconds), tick_samples),
                    range(tick_samples, int(sample_rate * nr_of_seconds), tick_samples)):
        aux = voice[i:j]

        plt.title("Matey travestitul")
        plot_voice_frame(aux)
        plt.draw()
        plt.pause(tick_in_seconds / 2)
        plt.clf()
    plt.close()


def random_search(id, n):
    plt.ion()

    voice_path = "File.wav"
    voice, sample_rate = load_song(voice_path)

    nr_of_seconds = len(voice) / sample_rate

    true_value = 18.27
    best_tick_in_seconds = None
    best_tick_in_seconds_error = 9999999999999999999999

    for _ in tqdm(range(n), position=id):
        tick_in_seconds = random.random()
        while tick_in_seconds == 0:
            tick_in_seconds = random.random()

        tick_samples = int(sample_rate * tick_in_seconds)

        current_score_error = timeit.timeit(
            lambda: plot_and_show_voice(voice, sample_rate, nr_of_seconds, tick_samples, tick_in_seconds), number=1)

        if abs(current_score_error - true_value) < best_tick_in_seconds_error:
            best_tick_in_seconds = tick_in_seconds
            best_tick_in_seconds_error = abs(current_score_error - true_value)

    return best_tick_in_seconds, best_tick_in_seconds_error


def get_best_tick():
    # NR DE CORE-URI
    nr_of_processes = 8

    n = 10 ** 3

    with Pool(nr_of_processes) as p:
        results = p.starmap(random_search, [(id, n // nr_of_processes) for id in range(nr_of_processes)])

    print(results)

    results = list(zip(*results))
    best_tick_in_seconds = results[0][np.argmin(np.array(results[1]))]
    best_tick_in_seconds_error = results[1][np.argmin(np.array(results[1]))]

    print(f"Best tick in seconds: {best_tick_in_seconds}\nBest tick in seconds error: {best_tick_in_seconds_error}")


def plot_voice():
    plt.ion()
    voice_path = "File.wav"

    voice, sample_rate = load_song(voice_path)
    nr_of_seconds = len(voice) / sample_rate
    tick_in_seconds = 0.04

    tick_samples = int(sample_rate * tick_in_seconds)
    os.startfile(voice_path)
    plot_and_show_voice(voice, sample_rate, nr_of_seconds, tick_samples, tick_in_seconds)


if __name__ == '__main__':
    # get_best_tick()
    print(timeit.timeit(plot_voice, number=1))

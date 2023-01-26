# functions to handle plotting
import numpy as np
import matplotlib.pyplot as plt

def plot_WAV_and_spectro(rate,data,seconds,channel=0):

    # takes sampling rate in HZ and WAV timeseries samples data

    # can choose how many seconds to plot, should be faster for shorter times

    # will focus on channel 0, later might need both channels 

    n = rate*seconds  # total points = rate Hz * 60 seconds 

    total_length = data.shape[0]/rate

    time = np.linspace(0., total_length, data.shape[0])


    dt = time[-1]-time[-2]

    NFFT = 1024  # the length of the windowing segments
    nover = 900  # overlap of windows


    Fs = int(1.0 / dt)  # the sampling frequency

    print(dt,Fs,n,n/NFFT)

    t = time[:n]

    x = data[:n,0]

    fig, (ax1, ax2) = plt.subplots(nrows=2)
    ax1.plot(t, x)
    Pxx, freqs, bins, im = ax2.specgram(x, NFFT=NFFT, Fs=Fs, noverlap=nover)
    # The `specgram` method returns 4 objects. They are:
    # - Pxx: the periodogram
    # - freqs: the frequency vector
    # - bins: the centers of the time bins
    # - im: the matplotlib.image.AxesImage instance representing the data in the plot

    ax1.set_xlim(0,seconds)
    ax2.set_xlim(0,seconds)

    #ax2.set_ylim(0,10000)

def get_spectrogram(rate,data,seconds,channel=0):

    n = rate*seconds # only look at clip of seconds length

    Fs = rate

    NFFT = 1024
    nover = 900

    x=data[:n,channel]

    plt.show('False')

    Pxx, freqs, bins, im = plt.specgram(x, NFFT=NFFT, Fs=Fs, noverlap=nover)

    return Pxx,freqs,bins

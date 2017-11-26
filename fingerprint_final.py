import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Audio, display
from matplotlib.mlab import specgram
from scipy.io import wavfile
from scipy import signal
from skimage.feature import peak_local_max
import wave
import pyaudio
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion, iterate_structure


window_size = 1024

def recorder(CHUNK = window_size,
                FORMAT = pyaudio.paInt16,
                CHANNELS = 1,
                RATE = 44100,
                RECORD_SECONDS = 5,
                WAVE_OUTPUT_FILENAME = "pyaudio_recording_final.wav"):

    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels= CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    print("recording stream")
    frames = []
    for i in range(0,int(RATE/CHUNK*RECORD_SECONDS)):
        data = stream.read(CHUNK,exception_on_overflow = False)
        frames.append(data)
    print("recording done")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf=wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def wav_reader(wav_file):
    rate, sample_array = wavfile.read(wav_file+'.wav')
    #sample_array = sample_array[:,0]
    return rate, sample_array

def locate_peaks(sample_array, rate, min_freq = 0, max_freq = 20000, min_distance = 20, threshold_abs = 20):
    spec, freqs, t = specgram(sample_array, NFFT= 1024, Fs=rate, noverlap=1024*0.5, pad_to = None)
    spec[spec == 0] = 1e-6
    Z_cut, freqs_cut = cut_specgram(min_freq, max_freq, spec, freqs)
    coordinates = peak_local_max(Z_cut, min_distance, threshold_abs)
    return coordinates, spec, freqs, t, Z_cut

def cut_specgram(min_freq, max_freq, spec, freqs):
    #returns magnitude of spectrum values between 0-15KHz
    spec_cut = spec[(freqs >= min_freq) & (freqs <= max_freq)]
    #returns frequency between 0-15KHz
    freqs_cut = freqs[(freqs >= min_freq) & (freqs <= max_freq)]
    #create a box around the magnitudes
    Z_cut = 10 * np.log10(spec_cut)
    #flip the array since imshow (0,0) is upper left
    Z_cut = np.flipud(Z_cut)
    Z_cut[Z_cut == -np.inf] = 0
    return Z_cut, freqs_cut

def show_peaks(spec, freqs, t, coord):
    Z = 10.0 * np.log10(spec)
    Z = np.flipud(Z)
    Z[Z == -np.inf] = 0
    fig = plt.figure(figsize=(10, 8), facecolor='white')
    #spec
    plt.imshow(Z, cmap = "hot")
    #peaks
    plt.scatter(coord[:, 1], coord[:, 0])
    #get current axis plots over current axis
    ax = plt.gca()
    #axis settings
    plt.xlabel('Time bin')
    plt.ylabel('Frequency')
    plt.title('peaks', fontsize=18)
    plt.axis('auto')
    ax.set_xlim([0, len(t)])
    ax.set_ylim([len(freqs), 0])
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    plt.show()

def example_peak_local_max():
        #Return coordinates of peaks in an image
        #Peaks are the local maxima in a region of 2 * min_distance + 1
        #(i.e. peaks are separated by at least min_distance).
        #http://scikit-image.org/docs/0.7.0/api/skimage.feature.peak.html
    im = np.zeros((7,7))
    im[3, 4] = 1
    im[3, 2] = 1.5
    print(im)
    print('with min_distance = 1: ', peak_local_max(im, min_distance = 1))
    print('with min_distance = 2: ', peak_local_max(im,min_distance = 2))

def specgram_plt(spec, freqs, t):
    fig1 = plt.figure(figsize=(10, 8), facecolor='white')
    extent = 0, np.amax(t), freqs[0], freqs[-1]
    Z = 10.0 * np.log10(spec)
    Z = np.flipud(Z)
    plt.imshow(Z, cmap='hot', extent=extent)
    plt.xlabel('Time bin')
    plt.ylabel('Frequency [Hz]')
    plt.title('song')
    plt.axis('auto')
    ax = plt.gca()
    ax.set_xlim([0, extent[1]])
    ax.set_ylim([freqs[0], freqs[-1]])
    plt.show()

def peaks_v2(image):
    image = 10 * np.log10(image)
    #flip the array since imshow (0,0) is upper left
    #image = np.flipud(image)
    image[image == -np.inf] = 0
    neighborhood = generate_binary_structure(2,1)
    #apply the local maximum filter; all pixel of maximal value
    #in their neighborhood are set to 1
    neighborhood = iterate_structure(neighborhood,20).astype(int)
    local_max = maximum_filter(image, footprint=neighborhood ) == image
    background = (image == 0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
    detected_peaks = local_max ^ eroded_background
    filter_peaks_v2(detected_peaks, image)

def filter_peaks_v2(detected_peaks, image):
    # threshold for amplitudes
    AMPLITUDE_THRESHOLD = 20

    # get amplitudes of peaks
    amplitudes = image[detected_peaks].flatten()
    y, x = detected_peaks.astype(int).nonzero()

    #zip tuples
    all_peaks = zip(x, y, amplitudes)
    filtered_peaks = [p for p in all_peaks if p[2] > AMPLITUDE_THRESHOLD]
    fingerprint = ( [p[0] for p in filtered_peaks],
                    [p[1] for p in filtered_peaks])
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    x, y = fingerprint[0], fingerprint[1]
    ax1.pcolor(image, cmap="hot")
    ax1.scatter(x, y, c= 'blue')
    plt.show()

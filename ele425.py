import soundfile as sf
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift
import numpy as np


data, samplerate = sf.read('/Users/nicknorden/Downloads/one_small_step.wav')
np_fft = np.fft.rfft(data*np.hanning(len(data)))
d = len(np_fft)/2

plt.figure(1)
plt.title("np/hanning")
plt.plot(abs(np_fft[:(d-1)]),'r')


plt.figure(2)

window = np.hanning(51) #input
plt.plot(window)
plt.title("Hann window")

plt.figure(3)
#normalized over half of the number of input samples 51 => 25.5
A = fft(window, 2048) / 25.5 #fft(array, length of fourier transform (optional))
mag = np.abs(fftshift(A))
freq = np.linspace(-0.5, 0.5, len(A))
response = 20 * np.log10(mag)
response = np.clip(response, -100, 100)
plt.plot(freq, response)

plt.title("Frequency response of the Hann window")

plt.ylabel("Magnitude [dB]")
plt.xlabel("Normalized frequency [cycles per sample]")
plt.axis('tight')

plt.figure(4)
E = fft(data)
mag1 = np.abs(E)
freq1 = np.linspace(0, 2048, len(E))
response1 = 20 * np.log10(mag1)
response1 = np.clip(response1, -100, 100)
plt.plot(freq1, response1)



plt.show()

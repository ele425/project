import fingerprint_final as fp


'''
records for 5 seconds at 16 bits, 44.1KHz, 1 channel, 1024 bit chunks...
some people use 4096 bit chunks which may help us reduce computations since the FFT
has to be the same sample/chunk length
'''
#fp.recorder()

rate, sample_array = fp.wav_reader('pyaudio_recording_final')
coordinates, spec, freqs, t, Z_cut = fp.locate_peaks(sample_array,rate)

'''
shows spectrogram of input
'''
#fp.specgram_plt(spec,freqs,t)

'''
two different ways to find peaks but apparently in the background the peak_local_max function goes through the exact
same process (i.e binary mask, dialation, background erosion) with enough tweaking they can find the same peaks.
However, peak_local_max (fp.locate_peaks) returns coordinates of the image in an array of pixels (x,y) not frequency
and time. Not sure if that matters since the pixel (x,y) should be the same as spec (freq,time).
'''
fp.show_peaks(spec, freqs, t, coordinates)
#fp.peaks_v2(spec)


'''
example of how peak_local_max works for different min_distances
'''
#fp.example_peak_local_max()

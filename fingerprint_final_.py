import fingerprint_final as fp

#fp.recorder()

rate, sample_array = fp.wav_reader('pyaudio_recording_final')
coordinates, spec, freqs, t, Z_cut, sorted_peak_coord = fp.locate_peaks(sample_array,rate)

#fp.specgram_plt(spec,freqs,t)
#fp.plot_peaks(spec, freqs, t, coordinates)

hashes = fp.generate_hashes(sorted_peak_coord)
print(hashes[:2])


'''
two different ways to find peaks but apparently in the background the peak_local_max function goes through the exact
same process (i.e binary mask, dialation, background erosion) with enough tweaking they can find the same peaks.
However, peak_local_max (fp.locate_peaks) returns coordinates of the image in an array of pixels (x,y) not frequency
and time. Not sure if that matters since the pixel (x,y) should be the same as spec (freq,time).
'''

'''
example of how peak_local_max works for different min_distances
'''
#fp.example_peak_local_max()

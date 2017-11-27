import fingerprint_final as fp
import hashPeaks as hp

#fp.recorder()

rate, sample_array = fp.wav_reader('one_small_step')
coordinates, spec, freqs, t, Z_cut, sorted_peak_coord = fp.locate_peaks(sample_array,rate)

#fp.specgram_plt(spec,freqs,t)
fp.plot_peaks(spec, freqs, t, coordinates)
hashes = hp.hash_fingerprints(sorted_peak_coord, 5)
print(hashes[:5])
hp.write_fingerprint("one small step small", hashes)
collisions = hp.find_collisions("one small step small", hashes)
print("Number of collisions: {0}".format(collisions))



#'d5adefb3aca94a7d8ede072ca08b83b3'
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

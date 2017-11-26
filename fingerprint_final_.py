import fingerprint_final as fp
import numpy as np
#fp.recorder()
rate, sample_array = fp.wav_reader('pyaudio_recording_final')
coordinates, spec, freqs, t, Z_cut = fp.locate_peaks(sample_array,rate)
fp.show_peaks(spec, freqs, t, coordinates)
#fp.example_peak_local_max()
#fp.specgram_plt(spec,freqs,t)

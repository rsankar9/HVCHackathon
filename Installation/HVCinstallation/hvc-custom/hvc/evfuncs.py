"""
ev_funcs
Python implementations of functions used with EvTAF and evsonganaly.m
"""

#from third-party
import numpy as np
from scipy.io import loadmat
import scipy.signal

# Test
import scipy as sp
# End test


#from hvc
import hvc.audiofileIO


def readrecf(filename):
    """
    reads .rec files output by EvTAF
    """

    rec_dict = {}
    with open(filename,'r') as recfile:
        line_tmp = ""
        while 1:
            if line_tmp == "":
                line = recfile.readline()
            else:
                line = line_tmp
                line_tmp = ""
                
            if line == "":  # if End Of File
                break
            elif line == "\n":  # if blank line
                continue
            elif "Catch" in line:
                ind = line.find('=')
                rec_dict['iscatch'] = line[ind+1:]
            elif "Chans" in line:
                ind = line.find('=')
                rec_dict['num_channels'] = int(line[ind+1:])
            elif "ADFREQ" in line:
                ind = line.find('=')
                try:
                    rec_dict['sample_freq'] = int(line[ind+1:])
                except ValueError:
                    rec_dict['sample_freq'] = float(line[ind+1:])
            elif "Samples" in line:
                ind = line.find('=')
                rec_dict['num_samples'] = int(line[ind+1:])
            elif "T After" in line:
                ind = line.find('=')
                rec_dict['time_after'] = float(line[ind+1:])
            elif "T Before" in line:
                ind = line.find('=')
                rec_dict['time before'] = float(line[ind+1:])
            elif "Output Sound File" in line:
                ind = line.find('=')
                rec_dict['outfile'] = line[ind+1:]
            elif "Thresholds" in line:
                th_list = []
                while 1:
                    line = recfile.readline()
                    if line == "":
                        break
                    try:
                        th_list.append(float(line))
                    except ValueError:  # because we reached next section
                        line_tmp = line
                        break
                rec_dict['thresholds'] = th_list
                if line == "":
                    break
            elif "Feedback information" in line:
                fb_dict = {}
                while 1:
                    line = recfile.readline()
                    if line == "":
                        break
                    elif line == "\n":
                        continue
                    ind = line.find("msec")
                    time = float(line[:ind-1])
                    ind = line.find(":")
                    fb_type = line[ind+2:]
                    fb_dict[time] = fb_type
                rec_dict['feedback_info'] = fb_dict
                if line == "":
                    break
            elif "File created" in line:
                header = [line]
                for counter in range(4):
                    line = recfile.readline()
                    header.append(line)
                rec_dict['header']=header
    return rec_dict


def load_cbin(filename,channel=0):
    """
    loads .cbin files output by EvTAF. 
    
    arguments
    ---------
    filename : string

    channel : integer
        default is 0

    returns
    -------
    data : numpy array
        1-d vector of 16-bit signed integers

    sample_freq : integer
        sampling frequency in Hz. Typically 32000.
    """
    
    # .cbin files are big endian, 16 bit signed int, hence dtype=">i2" below
    data = np.fromfile(filename,dtype=">i2")
    recfile = filename[:-5] + '.rec'
    rec_dict = readrecf(recfile)
    data = data[channel::rec_dict['num_channels']]  # step by number of channels
    sample_freq = rec_dict['sample_freq']
    return data, sample_freq


def load_notmat(filename):
    """
    loads .not.mat files created by evsonganaly.m.
    wrapper around scipy.io.loadmat.
    Calls loadmat with squeeze_me=True to remove extra dimensions from arrays
    that loadmat parser sometimes adds.
    
    Argument
    --------
    filename : string, name of .not.mat file
     
    Returns
    -------
    notmat_dict : dictionary of variables from .not.mat files
    """

    if ".not.mat" in filename:
        pass
    elif filename[-4:] == "cbin":
            filename += ".not.mat"
    else:
        raise ValueError("Filename should have extension .cbin.not.mat or"
                         " .cbin")

    return loadmat(filename, squeeze_me=True)


def get_syls(cbin, spect_params, labels_to_use='all', syl_spect_width=-1):
    """
    Get birdsong syllables from .cbin files using the associated
    .cbin.not.mat file generated by evsonganaly.m (and the person that
    labeled the song).

    Parameters
    ----------
    cbin : string
        .cbin filename
    spect_params: dictionary
        with keys 'nperseg','noverlap','freq_cutoffs', and 'samp_freq'.
        Note that 'samp_freq' is the **expected** sampling frequency and the
        function throws an error if the actual sampling frequency of cbin does
        not match the expected one.
    labels_to_use : list or string
        List or string of all labels for which associated spectrogram should be made.
        When called by extract, this function takes a list created by the
        extract config parser. But a user can call the function with a string.
        E.g., if labels_to_use = 'iab' then syllables labeled 'i','a',or 'b'
        will be extracted and returned, but a syllable labeled 'x' would be
        ignored. If labels_to_use=='all' then all spectrograms are returned with
        empty strings for the labels. Default is 'all'.
    syl_spect_duration : int
        Optional parameter to set constant duration for each spectrogram of a
        syllable, in seconds. E.g., 0.05 for an average 50 millisecond syllable. 
        Used for creating inputs to neural network where each input
        must be of a fixed size.
        Default value is -1; in this case, the width of the spectrogram will
        be the duration of the spectrogram as determined by the segmentation
        algorithm in evsonganaly.m, i.e. the onset and offset that are stored
        in the .cbin.not.mat file.
        If a different value is given, then the duration of each spectrogram
        will be that value. Note that if any individual syllable has a duration
        greater than syl_spect_duration, the function raises an error.

    Returns
    -------
    all_syls : list of syllable objects
        see hvc.audio for definition of syllable class
    all_syl_labels : list of chars
    """

    if labels_to_use != 'all':
        if type(labels_to_use) !=list and type(labels_to_use) != str:
            raise ValueError('labels_to_use argument should be a list or string')
        if type(labels_to_use) == str:
            labels_to_use = list(labels_to_use)

    dat, samp_freq = load_cbin(cbin)
    if samp_freq != spect_params['samp_freq']:
        raise ValueError(
            'Sampling frequency for {}, {}, does not match expected sampling '
            'frequency of {}'.format(cbin,
                                     samp_freq,
                                     spect_params['samp_freq']))

    notmat = load_notmat(cbin)
    onsets_Hz = np.round((notmat['onsets'] / 1000) * samp_freq).astype(int)
    offsets_Hz = np.round((notmat['offsets'] / 1000) * samp_freq).astype(int)
    if syl_spect_width > 0:
        syl_spect_width_Hz = np.round(syl_spect_width * samp_freq)

    all_labels = []
    all_syls = []

    for ind, (label, onset, offset) in enumerate(zip(notmat['labels'],onsets_Hz,offsets_Hz)):
        if 'syl_spect_width_Hz' in locals():
            syl_duration_in_samples = offset - onset
            if syl_duration_in_samples < syl_spect_width_Hz:
                raise ValueError('syllable duration of syllable {} with label {}'
                                 'in file {} is greater than '
                                 'width specified for all syllable spectrograms.'
                                 .format(ind,label,cbin))

        if labels_to_use == 'all':
            label = None
        elif label not in labels_to_use:
            continue
        all_labels.append(label)

        if 'syl_spect_width_Hz' in locals():
            width_diff = syl_spect_width_Hz - syl_duration_in_samples
            # take half of difference between syllable duration and spect width
            # so one half of 'empty' area will be on one side of spect
            # and the other half will be on other side
            # i.e., center the spectrogram
            left_width = int(round(width_diff / 2))
            right_width = width_diff - left_width
            if left_width > onset: # if duration before onset is less than left_width
                # (could happen with first onset)
                left_width = 0
                right_width = width_diff - offset
            elif offset + right_width > dat.shape[-1]:
                # if right width greater than length of file
                right_width = dat.shape[-1] - offset
                left_width = width_diff - right_width
            syl_audio = dat[:, onset - left_width:
                             offset + right_width]
        else:
            syl_audio = dat[onset:offset]
        syllable = hvc.audiofileIO.make_syl_spect(syl_audio,
                                                  samp_freq,
                                                  nfft=spect_params['nperseg'],
                                                  overlap=spect_params['noverlap'],
                                                  freq_cutoffs = spect_params['freq_cutoffs'][0])
        all_syls.append(syllable)

    return all_syls, all_labels


def bandpass_filtfilt(rawsong, samp_freq, freq_cutoffs=(500, 10000)):
    """filter song audio with band pass filter, run through filtfilt
    (zero-phase filter)

    Parameters
    ----------
    rawsong : ndarray
        audio
    samp_freq : int
        sampling frequency
    freq_cutoffs : list
        2 elements long, cutoff frequencies for bandpass filter.
        If None, no cutoffs; filtering is done with cutoffs set
        to range from 0 to the Nyquist rate.
        Default is [500, 10000].

    Returns
    -------
    filtsong : ndarray
    """
	
    # Test versions libraries
    #print(np.__version__)

    #print(sp.__version__)

    #Accessoirement, tu peux tester les 2 libraires:
    ##np.test()
    ##sp.test()

    #Tu peux aussi tester quel BLAS / LAPACK est installé avec:
    #np.show_config()
    # End Test versions libraries
	
	
    if freq_cutoffs[0] <= 0:
        raise ValueError('Low frequency cutoff {} is invalid, '
                         'must be greater than zero.'
                         .format(freq_cutoffs[0]))

    Nyquist_rate = samp_freq / 2
    if freq_cutoffs[1] >= Nyquist_rate:
        raise ValueError('High frequency cutoff {} is invalid, '
                         'must be less than Nyquist rate, {}.'
                         .format(freq_cutoffs[1], Nyquist_rate))

    if rawsong.shape[-1] < 387:
        numtaps = 64
    elif rawsong.shape[-1] < 771:
        numtaps = 128
    elif rawsong.shape[-1] < 1539:
        numtaps = 256
    else:
        numtaps = 512

    cutoffs = np.asarray([freq_cutoffs[0] / Nyquist_rate,
                          freq_cutoffs[1] / Nyquist_rate])
    # code on which this is based, bandpass_filtfilt.m, says it uses Hann(ing)
    # window to design filter, but default for matlab's fir1
    # is actually Hamming
    # note that first parameter for scipy.signal.firwin is filter *length*
    # whereas argument to matlab's fir1 is filter *order*
    # for linear FIR, filter length is filter order + 1
    b = scipy.signal.firwin(numtaps + 1, cutoffs, pass_zero=False)
    a = np.zeros((numtaps+1,))
    a[0] = 1  # make an "all-zero filter"
    padlen = np.max((b.shape[-1] - 1, a.shape[-1] - 1))
    filtsong = scipy.signal.filtfilt(b, a, rawsong, padlen=padlen)
    return filtsong


# Initial default for smooth_win = 2
def smooth_data(rawsong, samp_freq, freq_cutoffs=None, smooth_win=10):
    """filter raw audio and smooth signal
    used to calculate amplitude.

    Parameters
    ----------
    rawsong : 1-d numpy array
        "raw" voltage waveform from microphone
    samp_freq : int
        sampling frequency
    freq_cutoffs: list
        two-element list of integers, [low freq., high freq.]
        bandpass filter applied with this list defining pass band.
        Default is None, in which case bandpass filter is not applied.
    smooth_win : integer
        size of smoothing window in milliseconds. Default is 2.

    Returns
    -------
    smooth : 1-d numpy array
        smoothed waveform

    Applies a bandpass filter with the frequency cutoffs in spect_params,
    then rectifies the signal by squaring, and lastly smooths by taking
    the average within a window of size sm_win.
    This is a very literal translation from the Matlab function SmoothData.m
    by Evren Tumer. Uses the Thomas-Santana algorithm.
    """

    if freq_cutoffs is None:
        # then don't do bandpass_filtfilt
        filtsong = rawsong
    else:
        filtsong = bandpass_filtfilt(rawsong, samp_freq, freq_cutoffs)

    squared_song = np.power(filtsong, 2)
    len = np.round(samp_freq * smooth_win / 1000).astype(int)
    h = np.ones((len,)) / len
    smooth = np.convolve(squared_song, h)
    offset = round((smooth.shape[-1] - filtsong.shape[-1]) / 2)
    smooth = smooth[offset:filtsong.shape[-1] + offset]
    return smooth

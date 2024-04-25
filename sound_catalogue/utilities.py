import os
import pandas as pd
import wave
import contextlib
import operator
from pydub import AudioSegment
import datetime
from tabulate import tabulate
import soundfile as sf
from pypam import signal
import matplotlib.pyplot as plt
from tqdm.auto import tqdm
import pathlib
import numpy as np
import scipy.signal
import random

file_path = pathlib.Path(r'//fs/SHARED/onderzoek/6. Marine Observation Center/Projects/SoundLib_VLIZ2024/sound_db_new/sound_bpns/labelled_db/sound_catalogue/tag_specific_annotations_renumbered')

def create_ID_list(fname):
    file = os.path.join(file_path, fname)
    df = pd.read_csv(file, sep="\t")
    # renumber Selections ID
    num_rows = len(df)
    id_num_pre = [i + 1 for i in range(num_rows // 2)]
    random.shuffle(id_num_pre) # HIDE IF I DONT WANT ANNOTATION PLOTTED IN RANDOM ORDER!
    #print(id_num_pre)
    return id_num_pre

def read_raven_txt(fname, sel_id):
    beg_time = end_time = min_freq = max_freq = og_file = ann_file_name = ann_path = tag = None ##ADDED
    #file_name = fname
    file = os.path.join(file_path, fname)
    df = pd.read_csv(file, sep="\t")
    ann_id = int(sel_id) # No need to convert input to integer if it's already an integer
    x = df[df['Selection'] == ann_id]
    #print(tabulate(x, headers='keys'))
    if not x.empty:
        beg_time = x.at[x.index[0], 'Begin Time (s)']
        end_time = x.at[x.index[0], 'End Time (s)']
        min_freq = x.at[x.index[0], 'Low Freq (Hz)']
        max_freq =  x.at[x.index[0], 'High Freq (Hz)']
        og_file = x.at[x.index[0], 'Begin File']
        ann_file_name = x.at[x.index[0], 'Annotation file']
        ann_path = x.at[x.index[0], 'Path']
        tag = fname.replace('.txt','')
        #print(beg_time, end_time, og_file, ann_file_name, ann_path, tag)
        print('File of origin:', og_file)
        #print('Selection ID: ', sel_id)
    else:
        print("DataFrame is empty. No rows match the condition.")

    return beg_time, end_time, min_freq, max_freq, og_file, ann_file_name, ann_path, tag

def wav_duration(beg_time, end_time, og_file, ann_path):
    duration_dict = {}
    ln_lst = []
    for fname in os.listdir(ann_path):
        if fname.endswith('.wav'):
            full_path = os.path.join(ann_path, fname)
            # print(full_path)
            with contextlib.closing(wave.open(full_path, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                duration_dict[fname] = duration
                ln_lst.append(duration)
    # find index of wav
    if og_file in duration_dict:
        index = list(duration_dict).index(og_file)
    # find duration of all files up until index
    sum = 0
    i = 0
    while i < index:
        sum = sum + operator.add(0, ln_lst[i])
        i = i + 1
    #print('seconds since beginning of all files: ', sum)
    # 'seconds since beginning of files to end of specified file:' ( i <= index:)
    # compute exact time event starts:
    # START TIME OF EVENT
    b_time = (beg_time - sum) - 0.1
    print('Start time of sound event: ', b_time, 'sec')
    # END TIME OF EVENT
    delta_time = end_time - beg_time
    e_time = (b_time + delta_time) + 0.2 #+ 0.1
    print('End time of sound event: ', e_time, 'sec')
    return b_time, e_time

# def wav_duration(beg_time, end_time, og_file, ann_path):
#     duration_dict = {}
#     ln_lst = []
#     index = -1  # Initialize index with a default value
#     for fname in os.listdir(ann_path):
#         if fname.endswith('.wav'):
#             full_path = os.path.join(ann_path, fname)
#             with contextlib.closing(wave.open(full_path, 'r')) as f:
#                 frames = f.getnframes()
#                 rate = f.getframerate()
#                 duration = frames / float(rate)
#                 duration_dict[fname] = duration
#                 ln_lst.append(duration)
#
#     # Check if og_file is in duration_dict
#     if og_file in duration_dict:
#         index = list(duration_dict).index(og_file)
#
#     # Calculate the sum of durations up to index
#     sum_duration = sum(ln_lst[:index + 1]) if index >= 0 else 0
#
#     # Compute start and end time
#     b_time = (beg_time - sum_duration) - 0.1
#     e_time = (b_time + (end_time - beg_time)) + 0.1
#
#     return b_time, e_time

def snip_snip(ann_path, og_file, b_time, e_time, output_dir_sn, output_file_name, sel_id):
    input_file = os.path.join(ann_path, og_file)
    with wave.open(input_file, 'rb') as wave_file:
        frame_rate = wave_file.getframerate()
        # Calculate the start and end frame positions
        start_frame = int(b_time * frame_rate)
        end_frame = int(e_time * frame_rate)
        # Set the file's frame position to the start position
        wave_file.setpos(start_frame)
        # Read frames from start to end position
        frames = wave_file.readframes(end_frame - start_frame)
    # Create an AudioSegment from the frames
    audio_segment = AudioSegment(
        frames,
        frame_rate=frame_rate,
        sample_width=wave_file.getsampwidth(),
        channels=wave_file.getnchannels())

    os.makedirs(output_dir_sn, exist_ok=True) # ensure output directory exists
    sn_name = output_file_name + '_' + sel_id
    sn_name_ex = sn_name + ".wav"
    output_file_sn = os.path.join(output_dir_sn, sn_name_ex)
    #print(output_file_sn)
    audio_segment.export(output_file_sn, format="wav") # export snip # output_file
    return sn_name, sn_name_ex, output_file_sn

def get_spectrogram(sn_name, output_file_sn, max_freq, min_freq, output_dir_sp):
    sig, sr = sf.read(output_file_sn)
    winsize = min(int(len(sig) / 2), int(128 * max_freq / (max_freq - min_freq)) * 2) #128
    hopsize = min(int((len(sig) - winsize) / 128), int(winsize / 2))
    f, t, sxx = scipy.signal.spectrogram(sig, fs=sr, window=('hamming'),
                                         nperseg=winsize,
                                         noverlap=winsize - hopsize, nfft=winsize,
                                         detrend=False,
                                         return_onesided=True, scaling='density', axis=-1,
                                         mode='magnitude')

    vmin = min(-40, -70) #-50, -60 / -30, -80 / -40, -80
    vmax = max(-40, -70)

    plt.pcolormesh(t, f/1000, 10 * np.log10(sxx), vmin=vmin, vmax=vmax, shading=None, cmap='binary') #shading='gouraud', None. cmap='binary', jet, plasma
    plt.ylabel('Frequency [kHz]',fontdict={'fontname': 'Georgia'})
    plt.xlabel('Time [sec]',fontdict={'fontname': 'Georgia'})
    plt.title(sn_name,fontdict={'fontname': 'Comic Sans'})
    #plt.colorbar(label='PSD [dB re 1 $\mu Pa^2 / Hz$]')
    #plt.show()
    plt.savefig(os.path.join(output_dir_sp, sn_name + '.png'))
    plt.close()

# NOT IN USE:
def plot_spec(output_dir_sn, output_file_sn, output_dir_sp,  sn_name, sn_name_ex): # NOT IN USE ATM!!!
    # define file
    file_path = output_dir_sn
    file_name = sn_name_ex
    file = os.path.join(file_path, file_name)
    # read file
    wav_file = sf.SoundFile(file)
    fs = wav_file.samplerate
    start_sample = 0
    end_sample = wav_file.frames
    snippet, _ = sf.read(file, start=start_sample, stop=min(end_sample, wav_file.frames))

    # plot spectrogram
    s = signal.Signal(snippet, fs=fs)
    s.spectrogram()
    nfft = 256 #512
    overlap = 0
    scaling = 'spectrum'  # mel??
    db = True
    force_calc = True  # Force recalculation of spectrogram
    show = False

    plt.rcParams.update(plt.rcParamsDefault)
    _, _, sxx = s.spectrogram(nfft=nfft, scaling=scaling, overlap=overlap, db=db, force_calc=force_calc)

    # Ensure vmin is less than or equal to vmax
    vmin = min(-200, -600)
    vmax = max(-200, -600)

    print("vmin inside plot_spec:", vmin)  # Add this line to track the value of vmin
    print("vmax inside plot_spec:", vmax)

    if scaling == 'density':
        label = r'PSD [dB re 1 $\mu Pa^2 / Hz$]'
    elif scaling == 'spectrum':
        label = r'Power Spectrum [dB re 1 $\mu Pa^2$]'

    cmap = plt.get_cmap('binary')  # binary, gist_yarg
    plt.pcolormesh(s.t, s.freq / 1000, sxx, vmin=vmin, vmax=vmax, shading='auto', cmap=cmap)  # Dividing freq by 1000
    # plt.colorbar(label=label)  # Removed colorbar
    plt.title(sn_name)
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [kHz]')  # Changed ylabel to kHz

    # save spectrogram
    save_name = sn_name
    name_path = os.path.join(output_dir_sp, save_name)
    plt.savefig(name_path)
    plt.close()

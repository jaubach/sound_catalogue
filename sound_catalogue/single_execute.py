'''
Obtain snippet and spectrogram of the inputted annotation ID from the inputted soundtype (txt)
'''

import utilities
from tag_specific_ann_files import crete_ann_files

# 1. execute read_txt()
if __name__ == "__main__":
    fname = input("Enter tag specific annotation file name: ")
    sel_id = input("Enter selection ID: ")
    beg_time, end_file, min_freq, max_freq, og_file, ann_file_name, ann_path, tag = utilities.read_raven_txt(fname, sel_id)

# 2. execute wav_duration()
b_time, e_time = utilities.wav_duration(beg_time, end_file, og_file, ann_path)

# 3. execute snip_snip()
output_dir_sn = '//fs/SHARED/onderzoek/6. Marine Observation Center/Projects/SoundLib_VLIZ2024/sound_db_new/sound_bpns/labelled_db/sound_catalogue/snippets'
sn_name, sn_name_ex, output_file_sn = utilities.snip_snip(ann_path, og_file, b_time, e_time, output_dir_sn, tag, sel_id)

# 4. execute get_spectrogram()
output_dir_sp = '//fs/SHARED/onderzoek/6. Marine Observation Center/Projects/SoundLib_VLIZ2024/sound_db_new/sound_bpns/labelled_db/sound_catalogue/spectrograms'
#utilities.plot_spec(output_dir_sn, output_file_sn, output_dir_sp,  sn_name, sn_name_ex)
utilities.get_spectrogram(sn_name, output_file_sn, max_freq, min_freq, output_dir_sp)

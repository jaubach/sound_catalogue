'''
Obtain snippet and spectrogram of random annotation IDs from the inputted soundtype (txt)
'''

import utilities

if __name__ == "__main__":
    fname = input("Enter tag specific annotation file name: ")
    # call ID list
    id_num_pre = utilities.create_ID_list(fname)
    # iterate over each selection ID
    for sel_id in id_num_pre:
        print("Current selection ID:", sel_id)
        beg_time, end_file, min_freq, max_freq, og_file, ann_file_name, ann_path, tag = utilities.read_raven_txt(fname,
                                                                                                                 str(sel_id))
        b_time, e_time = utilities.wav_duration(beg_time, end_file, og_file, ann_path)
        output_dir_sn = '//fs/SHARED/onderzoek/6. Marine Observation Center/Projects/SoundLib_VLIZ2024/sound_db_new/sound_bpns/labelled_db/sound_catalogue/snippets'
        sn_name, sn_name_ex, output_file_sn = utilities.snip_snip(ann_path, og_file, b_time, e_time, output_dir_sn, tag,
                                                                  str(sel_id))
        output_dir_sp = '//fs/SHARED/onderzoek/6. Marine Observation Center/Projects/SoundLib_VLIZ2024/sound_db_new/sound_bpns/labelled_db/sound_catalogue/spectrograms'
        utilities.get_spectrogram(sn_name, output_file_sn, max_freq, min_freq, output_dir_sp)

'''
Output average duration, max freq, and min freq of each sound type into csv file
'''

import pandas as pd
import pathlib

folder = pathlib.Path(r'\\fs\SHARED\onderzoek\6. Marine Observation Center\Projects\SoundLib_VLIZ2024\sound_db_new\sound_bpns\labelled_db\sound_catalogue\tag_specific_annotations_renumbered')

csv = pd.DataFrame(columns=['number of individual annotations', 'avg min freq (Hz)', 'avg max freq (Hz)', 'avg time duration (s)'])

for txt_file in folder.glob('*.txt'):
    df = pd.read_csv(txt_file, sep="\t")
    soundtype_name = txt_file.name.split('.')[0]
    num_annots = len(pd.read_table(txt_file))//2
    min_freq = df['Low Freq (Hz)'].mean(skipna=True)
    max_freq = df['High Freq (Hz)'].mean(skipna=True)
    delta_time = (df['End Time (s)'] - df['Begin Time (s)']).mean(skipna=True)
    csv.loc[soundtype_name] = num_annots, min_freq, max_freq, delta_time

csv.to_csv(r'\\fs\SHARED\onderzoek\6. Marine Observation Center\Projects\SoundLib_VLIZ2024\sound_db_new\sound_bpns\labelled_db\sound_catalogue\sound_type_description.csv')




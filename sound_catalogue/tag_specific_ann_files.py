'''
Group each soundtype from all selection tables into soundtype specific txt files
'''

import pandas as pd
import pathlib
import os
from tabulate import tabulate

tag_lst = ['boat_noise',
           'boat_operations',
           'boat_sound',
           'chip',
           'composite_call',
           'croak',
           'crustacean_stridulation',
           'electronic_impact',
           'fish',
           'fish_grunt',
           'fish_knock',
           'impulsive_clack',
           'impulsive_clacks',
           'impulsive_click',
           'impulsive_clicks',
           'impulsive_impact',
           'impulsive_knock',
           'impulsive_poc',
           'impulsive_tic',
           'impulsive_tic_tac',
           'impulsive_tic_toc',
           'jackhammer',
           'knock',
           'kwa',
           'metallic_bell',
           'metallic_sound',
           'mouthbubble',
           'siren',
           'snitch',
           'stridulation',
           'tick',
           'water_movement',
           'whistle',
           'whistle_sound',
           'whistling']

path_input = pathlib.Path(
    r'//fs/SHARED/onderzoek/6. Marine Observation Center/Projects/SoundLib_VLIZ2024/sound_db_new/sound_bpns/labelled_db/selection_tables/temps_tests')
path_output = '//fs/SHARED/onderzoek/6. Marine Observation Center/Projects/SoundLib_VLIZ2024/sound_db_new/sound_bpns/labelled_db/sound_catalogue/tag_specific_annotations_renumbered'

def crete_ann_files():
    for tag in tag_lst:
        result_df = pd.DataFrame()
        for file in path_input.iterdir():
            df = pd.read_csv(file, sep="\t")
            # get annotation file name
            full_fname = file.name
            # get path of annotation file
            if "PhD_Clea" in full_fname:
                ann_path = full_fname.replace('Selection___', "//").replace('.txt', "")
                ann_path = ann_path.replace("_", '/', 4)
                reversed_txt = ann_path[::-1]
                reversed_txt = reversed_txt.replace("_", '/', 2)
                ann_path = reversed_txt[::-1]
                ann_path = ann_path[:38] + '/' + ann_path[39:]
                ann_path = ann_path[:15] + '_' + ann_path[16:]

            if "COVID-19" in full_fname:
                ann_path = full_fname.replace('Selection___', "//").replace('.txt', "")
                ann_path = ann_path.replace("_", '/', 5)
                reversed_txt = ann_path[::-1]
                reversed_txt = reversed_txt.replace("_", '/', 1)
                ann_path = reversed_txt[::-1]
                ann_path = ann_path[:15] + '_' + ann_path[16:]

            if '_complete' in full_fname:
                ann_path = full_fname.replace('Selection___', "//").replace('.txt', "")
                ann_path = ann_path.replace("_", '/', 4)
                reversed_txt = ann_path[::-1]
                reversed_txt = reversed_txt.replace("_", '/', 2)
                ann_path = reversed_txt[::-1]
                ann_path = ann_path[:38] + '/' + ann_path[39:]
                num_index = ann_path.find("210317")
                ann_path = ann_path[:num_index + len("210317")]
                ann_path = ann_path[:58] + '/' + ann_path[59:]
                ann_path = ann_path[:15] + '_' + ann_path[16:]

            elif "mono1" in full_fname:
                ann_path = full_fname.replace('Selection___', "//").replace('.txt', "")
                ann_path = ann_path.replace("_", '/', 5)
                reversed_txt = ann_path[::-1]
                reversed_txt = reversed_txt.replace("_", '/', 1)
                ann_path = reversed_txt[::-1]
                ann_path = ann_path[:15] + '_' + ann_path[16:]
                ann_path = ann_path[:58] + '/' + ann_path[59:]
                buitenratel_index = ann_path.find("Buitenratel")
                ann_path = ann_path[:buitenratel_index + len("Buitenratel")]

            # add columns
            if df['Tags'].isin([tag]).any():
                filtered_rows = df[df['Tags'] == tag]
                filtered_rows['Annotation file'] = full_fname
                filtered_rows['Path'] = ann_path
                if result_df.empty:
                    result_df = filtered_rows.copy()
                else:
                    result_df = pd.concat([result_df, filtered_rows],
                                          ignore_index=True)  # Concatenate with existing DataFrame

        # create csv
        result_df.to_csv(os.path.join(path_output, f'{tag}.txt'), sep='\t', index=False)

#crete_ann_files()
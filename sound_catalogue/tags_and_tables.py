'''
See in which selection tables each soundtype is present
'''

my_file = open("//fs/SHARED/onderzoek/6. Marine Observation Center/Projects/SoundLib_VLIZ2024/sound_db_new/sound_bpns/vliz_labelled_db/sound_catalogue/unique_sound_names.txt", "r")
data = my_file.read()
tag_list = data.replace('\n', ',').split(",")

for tag in tag_list:
    # print(tag)
    f = open("//fs/SHARED/onderzoek/6. Marine Observation Center/Projects/SoundLib_VLIZ2024/sound_db_new/sound_bpns/vliz_labelled_db/sound_catalogue/tags_and_tables.txt", "a")
    f.write(tag+'\n')
    os.chdir("//fs/SHARED/onderzoek/6. Marine Observation Center/Projects/SoundLib_VLIZ2024/sound_db_new/sound_bpns/vliz_labelled_db/selection_tables")
    for file in glob.glob("Selection*.txt"):
        df = pd.read_csv(file, sep="\t", header=None)
        new_header = df.iloc[0]
        df = df[1:]
        df.columns = new_header
        isin = df["Tags"].isin([tag]).tolist()
        if True in isin:
            f.write(file+'\n')
    f.close()
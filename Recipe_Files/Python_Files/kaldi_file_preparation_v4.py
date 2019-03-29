import pandas as pd
from pydub import AudioSegment
import os
from random import shuffle
from sklearn.model_selection import train_test_split
import sys

AIR_dir = sys.argv[1]

spk_list = ['FA','FB','MA','MB','MC']
spk_list.sort()

experiment_type = 'PER'

#text_files_dir = AIR_dir+'/Bulk_Data/One_Hour_FA_exp/phoneme_text/'
#audio_files_dir = AIR_dir+'/Bulk_Data/One_Hour_FA_exp/audio/'

text_files_dir = AIR_dir+'/Bulk_Data/Complete_Data/phoneme_text/'
audio_files_dir = AIR_dir+'/Bulk_Data/Complete_Data/audio/'

split_cat = ['dev']


# # Text

# ## Before running from here, make sure train.uttids and test.uttids is copied from dataset folder to bulk data kaldi files folder
def removeSpecialCharacters(string):
    charac_list = [".","-","–","_",";",":","‘","’","“",",","”","'","`","?","\"","[","]","@"]

    for charac in charac_list:
        if charac in string:
            string = string.replace(charac, " ")

    string = string.lstrip()
    string = string.rstrip()
    string = ' '.join(string.split())

    return string

for x in split_cat:
    ref_file = open(AIR_dir+'/Bulk_Data_Kaldi_Files/PER/'+x+'.uttids','r')
    ref_file_content = ref_file.read().split('\n')
    ref_file_content.remove('')

    temp_list = []
    for item in ref_file_content:
        file_name = item[:6]
        folder_name = item[7:]

        split_file = open(text_files_dir+folder_name+'/'+file_name+'.txt','r')
        s_f_content = split_file.read().split('\n')
        s_f_content = list(filter(lambda a: a != '', s_f_content))

        temp_str = item+' '
        for line in s_f_content:
            #filetered_line = removeSpecialCharacters(line)
            if line != s_f_content[-1]:
                temp_str = temp_str + line + ' '
            else:
                temp_str = temp_str + line

        temp_str = ' '.join(temp_str.split())

        temp_str = temp_str.replace("32 ","")
        temp_str = temp_str.replace(" 32","")
        temp_str = temp_str.replace("32","")

        temp_str = temp_str.replace("34 ","")
        temp_str = temp_str.replace(" 34","")
        temp_str = temp_str.replace("34","")

        temp_str = temp_str.replace("IE","I E")
        temp_str = temp_str.replace("IPA","I PA")

        temp_list.append(temp_str)
        split_file.close()
    temp_list.sort()


    file = open(AIR_dir+'/Bulk_Data_Kaldi_Files/PER/'+x+'.text','w')
    for item in temp_list:
        file.write(item+'\n')
    file.close()
    ref_file.close()


# # utt2spk
for x in split_cat:
    ref_file = open(AIR_dir+'/Bulk_Data_Kaldi_Files/PER/'+x+'.uttids','r')
    ref_file_content = ref_file.read().split('\n')
    ref_file_content.remove('')

    temp_list = []
    for item in ref_file_content:
        spk = item[:2]
        temp_str = item+' '+spk
        temp_list.append(temp_str)
    temp_list.sort()

    file = open(AIR_dir+'/Bulk_Data_Kaldi_Files/PER/'+x+'.utt2spk','w')
    for item in temp_list:
        file.write(item+'\n')
    file.close()
    ref_file.close()


# # spk2utt
for x in split_cat:
    ref_file = open(AIR_dir+'/Bulk_Data_Kaldi_Files/PER/'+x+'.utt2spk','r')
    ref_file_content = ref_file.read().split('\n')
    ref_file_content.remove('')

    spk2utt_dict = {}
    for spk in spk_list:
        spk2utt_dict[spk] = []

    for item in ref_file_content:
        spk = item.split(' ')[1]
        spk2utt_dict[spk].append(item.split(' ')[0])

    file = open(AIR_dir+'/Bulk_Data_Kaldi_Files/PER/'+x+'.spk2utt','w')
    for spk in spk_list:
        utt_list = spk2utt_dict[spk]

        temp_str = spk
        for utt in utt_list:
            temp_str = temp_str+' '+utt
        temp_str = temp_str+'\n'

        file.write(temp_str)
    file.close()
    ref_file.close()


# # spk2gender
temp_list = []
for spk in spk_list:
    gender = spk[0].lower()
    temp_str = spk+' '+gender+'\n'
    temp_list.append(temp_str)
temp_list.sort()

for x in split_cat:
    file = open(AIR_dir+'/Bulk_Data_Kaldi_Files/PER/'+x+'.spk2gender','w')
    for item in temp_list:
        file.write(item)
    file.close()


# # wav.scp
#wav_file_path = AIR_dir+'/Bulk_Data/One_Hour_FA_exp/audio/'
wav_file_path = AIR_dir+'/Bulk_Data/Complete_Data/audio/'

for x in split_cat:
    ref_file = open(AIR_dir+'/Bulk_Data_Kaldi_Files/PER/'+x+'.uttids','r')
    ref_file_content = ref_file.read().split('\n')
    ref_file_content.remove('')

    temp_list = []
    for item in ref_file_content:
        file_name = item[:6]
        folder_name = item[7:]

        temp_str = item+' '+wav_file_path+folder_name+'/'+file_name+'.wav\n'

        temp_list.append(temp_str)
    temp_list.sort()

    file = open(AIR_dir+'/Bulk_Data_Kaldi_Files/PER/'+x+'_wav.scp','w')
    for item in temp_list:
        file.write(item)
    file.close()
    ref_file.close()


# # Duration file
for x in split_cat:
    ref_file = open(AIR_dir+'/Bulk_Data_Kaldi_Files/PER/'+x+'.uttids','r')
    ref_file_content = ref_file.read().split('\n')
    ref_file_content.remove('')

    temp_list = []
    for item in ref_file_content:
        file_name = item[:6]
        folder_name = item[7:]

        audio_file = AudioSegment.from_wav(audio_files_dir+folder_name+'/'+file_name+'.wav')

        temp_str = item+' '+str(audio_file.duration_seconds)+'\n'
        temp_list.append(temp_str)
    temp_list.sort()

    file = open(AIR_dir+'/Bulk_Data_Kaldi_Files/PER/'+x+'_dur.ark','w')
    for item in temp_list:
        file.write(item)
    file.close()
    ref_file.close()

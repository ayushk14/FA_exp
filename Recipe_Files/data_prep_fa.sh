#!/bin/bash

. ./cmd.sh
[ -f path.sh ] && . ./path.sh
set -e

AIR_dataset_dir=$1
AIR_receipe_dir=`pwd`
g2p_tool_dir=$AIR_dataset_dir/Tools/g2p/Kannadag2p/src

data_dir=data/local/data
dict_dir=data/local/dict
kaldi_files_dir=$AIR_dataset_dir/Bulk_Data_Kaldi_Files/PER
mkdir -p $data_dir $dict_dir $kaldi_files_dir

#rm $AIR_dataset_dir/Bulk_Data_Kaldi_Files/lexicon.txt
#rm $AIR_dataset_dir/Bulk_Data_Kaldi_Files/phones.txt
#rm $AIR_dataset_dir/Bulk_Data_Kaldi_Files/dev.uttids

cp -a ~/FA_exp/Recipe_Files/dict_files/lexicon.txt $AIR_dataset_dir/Bulk_Data_Kaldi_Files/lexicon.txt
cp -a ~/FA_exp/Recipe_Files/dict_files/phones.txt $AIR_dataset_dir/Bulk_Data_Kaldi_Files/phones.txt
cp -a ~/FA_exp/Recipe_Files/dev.uttids $AIR_dataset_dir/Bulk_Data_Kaldi_Files/dev.uttids

python3 Python_Files/kaldi_file_preparation_v4.py $AIR_dataset_dir
echo "Train files preparation done!!!!"
echo "Copying files created to AIR receipe...."

cp -a $AIR_dataset_dir/Bulk_Data_Kaldi_Files/dev_dur.ark ./$data_dir/
cp -a $AIR_dataset_dir/Bulk_Data_Kaldi_Files/dev.spk2utt ./$data_dir/
cp -a $AIR_dataset_dir/Bulk_Data_Kaldi_Files/dev.utt2spk ./$data_dir/
cp -a $AIR_dataset_dir/Bulk_Data_Kaldi_Files/dev_wav.scp ./$data_dir/
cp -a $AIR_dataset_dir/Bulk_Data_Kaldi_Files/dev.text ./$data_dir/
cp -a $AIR_dataset_dir/Bulk_Data_Kaldi_Files/dev.uttids ./$data_dir/
cp -a $AIR_dataset_dir/Bulk_Data_Kaldi_Files/dev.spk2gender ./$data_dir/


cp -a $AIR_dataset_dir/Bulk_Data_Kaldi_Files/lexicon.txt ./$dict_dir/
cp -a $AIR_dataset_dir/Bulk_Data_Kaldi_Files/phones.txt ./$dict_dir/

echo "Data and Dict files copied to AIR receipe!!!!"

#Below command create words.txt
#cat $AIR_dataset_dir/kaldi_files/train.text $AIR_dataset_dir/kaldi_files/test.text > $AIR_dataset_dir/kaldi_files/all.txt
#cut -d ' ' -f 2- $AIR_dataset_dir/kaldi_files/all.txt | sed 's/ /\n/g' | sort -u > $AIR_dataset_dir/kaldi_files/words.txt

#rm $AIR_dataset_dir/kaldi_files/all.txt

# Creating lexicon.txt and phones.txt using java g2p code
# At present, doing it manually
#cd $g2p_tool_dir

#javac Phoneme.java
#javac G2P_Base.java
#javac -encoding UTF-8 G2P_Kan.java
#javac -encoding UTF-8 create_lexicon.java
#javac create_lexicon.java

#java create_lexicon

#python3 Python_Files/create_unique_phones.py $AIR_dataset_dir
#echo "Lexicon and list of phones created!!!!"
#echo "Copying both files to AIR receipe...."

#cp -a $AIR_dataset_dir/kaldi_files/lexicon.txt ./$dict_dir/
#cp -a $AIR_dataset_dir/kaldi_files/phones.txt ./$dict_dir/
#echo "Files copied to AIR receipe!!!!"

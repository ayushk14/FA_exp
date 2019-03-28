#!/bin/bash

export USER=$(whoami)

cp -a Recipe_Files/Python_Files/kaldi_file_preparation_v4.py ~/kaldi/egs/AIR_Noisy_Worstcase_PER/s5/Python_Files/kaldi_file_preparation_v4.py

cp -a Recipe_Files/timit_format_data_fa.sh ~/kaldi/egs/AIR_Noisy_Worstcase_PER/s5/local_custom/timit_format_data_fa.sh

cp -a Recipe_Files/data_prep_fa.sh ~/kaldi/egs/AIR_Noisy_Worstcase_PER/s5/local_custom/data_prep_fa.sh

cp -a Recipe_Files/create_glm_stm_fa.sh ~/kaldi/egs/AIR_Noisy_Worstcase_PER/s5/local_custom/create_glm_stm_fa.sh

cd ~/kaldi/egs/AIR_Noisy_Worstcase_PER/s5

exit 0

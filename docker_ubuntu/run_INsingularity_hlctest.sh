#!/bin/bash

# run the script inside a singularity container.
# before running this script, need to set environment using 'env_setting.sh'

# I test this setting and environment on our workstation (Cryo03) in /home/hlctest/test_singularity_landuse_dl

#authors: Huang Lingcao
#email:huanglingcao@gmail.com
#add time: 25 November, 2019

## run exe.sh or other script with the environment of singularity
# to install packages, environment setting inside the container
exe_script=./setting_in_sing.sh

# run data preparing, training, inference, and post processing
#exe_script=./exe.sh

sing_dir=/home/hlctest/test_singularity_landuse_dl
sing_img=${sing_dir}/ubuntu16.04_itsc_tf.simg

# set mount disk on Cryo03 (need change when the machine setting is different)
export SINGULARITY_BINDPATH=/500G:/500G,/DATA1:/DATA1,/home/hlc:/home/hlc

env_home=${sing_dir}/packages

# set environment 
SINGULARITYENV_HOME=${sing_dir}/packages \
SINGULARITYENV_TZ=Asia/Hong_Kong \
SINGULARITYENV_PATH=${env_home}/bin:${env_home}/programs/miniconda2/bin:$PATH \
SINGULARITYENV_GDAL_DATA=${env_home}/programs/miniconda2/share/gdal \
SINGULARITYENV_LD_LIBRARY_PATH=${env_home}/programs/cuda-9.0/lib64:${env_home}/programs/cuDNN_7.0/cuda/lib64:${env_home}/programs/miniconda2/lib:$LD_LIBRARY_PATH \
singularity exec --nv ${sing_img} ${exe_script}






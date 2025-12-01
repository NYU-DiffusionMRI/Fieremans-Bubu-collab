#!/usr/bin/bash

# =============================================STEP 0=================================================
# A) Get access to ultraviolet
# B) Ask hcp admins to allow you to mount your labspace to bigpurple (http://bigpurple-ws.nyumc.org/wiki/index.php/Data-Management#Requesting_CIFS.2FSMB_Share_on_Data_Mover_Nodes)
# 
# C) In your terminal, after you ssh to bigpurple/ultraviolet, you may want to just run the following lines first:
# Pulling the docker may take up to an hour. Try again if it fails.

# module purge
# module load singularity/3.9.8
# module load cuda/11.8
# singularity pull docker://nyudiffusionmri/designer2:v2.0.15
# =====================================================================================================


# =============================================STEP 1=================================================
# A) Run the following so you can mount your labspace/research drive: 
# `srun -p data_mover -n 5 --mem-per-cpu=15G --time=2:00:00 --pty bash`
# B) Mount your labspace (eg /mnt/<kid>/bubulabspace)
# C) Copy data, scripts, and files you'll need to run designer from your labspace on to bigpurple/ultraviolet eg. designer_sing_cuda.batch
# =====================================================================================================


# =============================================STEP 2==================================================
# submit this file as a bash script not sbatch to wrap and submit as a bash script alone eg `bash designer_wrapper.sh`
scripts=/gpfs/path/to/scripts/and/idx/files

#list of .txt files containing subject IDs
#in this case, there are 3 .txt files and this script will send
#designer_sing_cuda.batch to run for these three in parallel
subj_txt=(ids_1.txt ids_2.txt ids_3.txt)


for i in ${subj_txt[@]}; do
    echo $i
    sbatch designer_sing_cuda.batch $scripts/$i
done

#Be careful of storage limitations on bigpurple
#I am not sure how many cases you can process at once
#check often and move data after processing

#If there are any bugs you are having a hard time fixing or adjusting, feel free to ask me for help (Jenny)
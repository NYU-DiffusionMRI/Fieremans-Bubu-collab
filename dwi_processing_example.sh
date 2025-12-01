#!/bin/bash

# Example call for running designer2 (from docker) on variable TE data

# ------------------------------------------------------------------------
# Path to the data
Main_Root="/mnt"
# Main_Root="/Volumes"
dwi_root=${Main_Root}"/labspace/Projects/PET-MR-CORE/BUBU/A_001/Baseline_2024_04_23"
dwi1=Head_ADNImMR_RMR_PA_b500_TE59_63SL_28.nii
dwi2=Head_ADNImMR_RMR_PA_b1000_TE76_63SL_14.nii
dwi3=Head_ADNImMR_PA_b2000short_TE98_63SL_22.nii
RPEname=Head_ADNImMR_RMR_AP_B1000_TE76_63SL_20.nii

# ------------------------------------------------------------------------
# Docker settings
docker_base_path="/data"

# ------------------------------------------------------------------------
# DESIGNER2 settings
preprocFolder="designer2"
mapsFolder="tmi"

# ------------------------------------------------------------------------
# DATA PRE-PROCESSING
docker run --rm --platform linux/amd64 -it -v "$dwi_root:$docker_base_path" -e FSLOUTPUTTYPE=NIFTI_GZ nyudiffusionmri/designer2:v2.0.15 \
designer -denoise -degibbs -eddy -nthreads 18 -rpe_pair "$docker_base_path/$RPEname" -rpe_te 0.076 -mask -scratch "$docker_base_path/${preprocFolder}/scratch" -nocleanup \
         -eddy_fakeb 1,1,1.5 -bshape 1,1,1 -echo_time 0.059,0.076,0.098 \
         "$docker_base_path/$dwi1","$docker_base_path/$dwi2","$docker_base_path/$dwi3" "$docker_base_path/${preprocFolder}/dwi_designer.nii"

# ------------------------------------------------------------------------
# PARAMETER ESTIMATION - (load_prior option)
docker run --rm --platform linux/amd64 -it -v "$dwi_root:$docker_base_path" -e FSLOUTPUTTYPE=NIFTI_GZ nyudiffusionmri/designer2:v2.0.15 \
tmi -DTI -DKI -WDKI -fit_constraints 0,0,0 -akc_outliers -fit_smoothing 10 -mask "$docker_base_path/${preprocFolder}/scratch/brain_mask.nii" \
    -SMI -select_prior SMI_Gaussian_wFWPrior.mat -compartments EAS,IAS,FW -sigma "$docker_base_path/${preprocFolder}/scratch/sigma.nii" \
    "$docker_base_path/${preprocFolder}/dwi_designer.nii" $docker_base_path"/$mapsFolder" 


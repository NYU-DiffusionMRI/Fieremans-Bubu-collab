# Fieremans-Bubu-collab
Diffusion MRI processing

- [Link to DESIGNER documentation](https://nyu-diffusionmri.github.io/DESIGNER-v2/)
- [Link to DOCKER documentation](https://hub.docker.com/u/nyudiffusionmri)

The current protocol contains the following data:
(i) TE = 59ms; b=0(2), 500(6) [s/mm^2]
(ii) TE = 76ms; b=0(2), 1000(40) [s/mm^2]
(iii) TE = 98ms; b=0(5), 500(6), 1000(12), 2000(48) [s/mm^2]

DTI & DKI maps will be computed for (i,ii,ii). The higher quality ones will be (iii) so use those for your analysis.
SMI maps will be computed using the full protocol. Note this is a white matter (WM) model so focus on WM regions of interest only.

Running designer:
- try the bash script 'dwi_processing_example.sh' which contains how to call designer2 and tmi using docker. Note we are using designer2:v2.0.15

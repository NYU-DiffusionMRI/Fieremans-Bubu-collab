#!/usr/bin/env python
# coding: utf-8
import os
import matplotlib.pyplot as plt
from glob import glob

import nibabel as ni
import numpy as np
from tqdm import tqdm



path_img='/path/to/folder/w/all/subjs/designer/outputs' #path to folder with all subjects' designer output
txt_path='path/to/txt/w/list/of/subj/ids/ids.txt' #path to txt with list of subjects
crs = open(os.path.join(txt_path), "r")
rows = (row.strip().split() for row in crs)
subjects = list(zip(*rows))[0]


roi_dir_ax='/path/to/qc/folder/qc' #path to where you want to save axial cuts png and html for QC
params=['rk_wdki','mk_wdki','ak_wdki','fa_dki','md_dki','ad_dki','rd_dki',
        'Da_smi','DePar_smi','DePerp_smi','f_smi','p2_smi'] #list of parameters. You can remove or add other parameters eg T2a_smi etc.
if not os.path.exists(roi_dir_ax):
    os.makedirs(roi_dir_ax)


#For each parameter
for p in params:
    print(p)
    #Plot axial slices for each subject
    for img_names in tqdm(subjects):
        # check if param map exists
        img_path=glob(os.path.join(path_img,img_names,'params','{}.nii'.format(p)))
        plt.style.use('dark_background')

        check = glob(os.path.join('{}/ax_{}_{}.png'.format(roi_dir_ax,img_names,p)))

        #initiate plots
        columns=5; rows=1
        fig, ax = plt.subplots(rows,columns,sharex=True,dpi=300)
        fig.subplots_adjust(hspace=0, wspace=0)

        #load maps
        img = ni.load(img_path[0])
        imgarray = np.array(img.dataobj)
        if 'smi' in p:
            fa_path=glob(os.path.join(path_img,img_names,'params','fa_dki.nii'))
            fa_img = ni.load(fa_path[0])
            fa_imgarray = np.array(fa_img.dataobj)
            imgarray[fa_imgarray<0.3]=np.nan

            b0_path=glob(os.path.join(path_img,img_names,'processing','b0bc.nii'))
            b0_img = ni.load(b0_path[0])
            b0_imgarray = np.array(b0_img.dataobj)
            c='hot'
        else:
            c='gray'

        shape = np.shape(imgarray)
        slices = shape[2]
        start=0.5
        #plot
        for i in range(columns):
            inc = i*0.03

            if 'smi' in p:
                b0 = b0_imgarray[:,:,int(np.ceil(slices*(start+inc)))]
                b0 = b0.swapaxes(-2,-1)[...,::-1,:]
                ax[i].imshow(b0,cmap='gray',vmin=0,vmax=1000)
            S = imgarray[:,:,int(np.ceil(slices*(start+inc)))]
            S = S.swapaxes(-2,-1)[...,::-1,:]
            ax[i].axes.xaxis.set_visible(False)
            ax[i].axes.yaxis.set_visible(False)
            ax[i].spines['top'].set_visible(False)
            ax[i].spines['right'].set_visible(False)
            ax[i].spines['bottom'].set_visible(False)
            ax[i].spines['left'].set_visible(False)
            if (p == 'fa_dki') or (p == 'DePerp_smi') or (p == 'f_smi') or (p == 'p2_smi') or (p == 'fw_smi'):
                simg=ax[i].imshow(S,cmap=c,vmin=0,vmax=1)
            elif p == 'p2_smi':
                simg=ax[i].imshow(S,cmap=c,vmin=0.1,vmax=1)
            elif (p == 'Da_smi') or (p == 'DePar_smi'):
                simg=ax[i].imshow(S,cmap=c,vmin=1,vmax=3)
            elif (p == 'T2a_smi') or (p == 'T2e_smi'):
                simg=ax[i].imshow(S,cmap=c,vmin=0,vmax=150)
            else:
                simg=ax[i].imshow(S,cmap=c,vmin=0,vmax=3)
            ymin, ymax = ax[i].get_ylim()
            xmin, xmax = ax[i].get_xlim()

            ax[i].set_ylim(ymin-int(0.05*abs(ymax-ymin)), ymax+int(0.05*abs(ymax-ymin)))
            ax[i].set_xlim(xmin+int(0.05*abs(xmax-xmin)), xmax-int(0.05*abs(xmax-xmin))) #ak
            ax[0].set_title(img_names, loc='center', pad=None)
            
        #save png with snapshot of the param map
        fig.colorbar(simg,ax=ax,orientation='horizontal',fraction=0.15,pad=0.03)
        fig.savefig('{}/ax_{}_{}.png'.format(roi_dir_ax,img_names,p),bbox_inches = "tight",dpi=1400)
        plt.close()




#Writing to HTML
for p in params:
    message="""<!DOCTYPE html>
    <html><body>"""
    message=message + '<div>'

    for imgs in tqdm(subjects):
        path_ax=sorted(glob(os.path.join(roi_dir_ax,'ax*{}*{}*.png'.format(imgs,p))))
        if path_ax:
            for i in range(len(path_ax)):
                ax=os.path.basename(path_ax[i])
                ax=path_ax[i]
                
                add_img_axial='<' + 'img src' + '=' + '"{}"'.format(ax) + 'alt="{}" height="150">'.format(ax)
                if (i % 2) != 0:
                    add_img=os.linesep + add_img_axial
                    message=message+add_img
                    message=message+'<div>'
                else:
                    add_img=add_img_axial
                    message=message+add_img

    message=message+'</body></html>'
    f = open('{}/{}.html'.format(roi_dir_ax,p),'w')

    f.write(message)
    f.close()


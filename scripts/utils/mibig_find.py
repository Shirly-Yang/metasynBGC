import os
from tqdm import tqdm
import sys

mibig=sys.argv[1]
mod=sys.argv[2]

pathGCF_list='GCF_select_list'

if mod == 'all':
    pathGCF_list='GCF_list'
pbar= tqdm(total=len(os.listdir(pathGCF_list)))
for i in os.listdir(pathGCF_list):
    #print(i)
    pathi=pathGCF_list+'/'+i
    filei=open(pathi,'r')
    linesi=filei.readlines()
    pbar.update(1)
    for l in linesi:
        if mibig in l:
            out=''.join([mibig,' in ',i,' with ',str(len(linesi)-1),' BGC.\n','Content:',l])
            print(out)
    filei.close()
pbar.close()

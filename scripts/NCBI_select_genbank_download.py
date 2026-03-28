import os
from NCBI_gbk_download  import entrez_url_fasta
from tqdm import tqdm
import random
import time
import sys

#pathout='NCBI_selected_fasta'
#pathin='GCF_select_list'
#GCF_number=sys.argv[1]+'.txt'
#pbar = tqdm(total=len(os.listdir(pathin)))
#n=0
#for i in os.listdir(pathin)[:1]:
    #i=GCF_number
    #n+=1
def GCF_fasta_download(i,pathin,pathout):
    print(i)
    print('BGC check and download')
    pathi=pathin+'/'+i
    filei=open(pathi,'r')
    linesi=filei.readlines()
    pbar = tqdm(total=len(linesi)-1)
    for l in linesi[1:]:
        NCBI_url=l.split('\t')[4]
        file_BGC_ID=pathout+'/'+l.split('\t')[0]+'.fasta'
        if NCBI_url != 'n/a':
            if os.path.exists(file_BGC_ID) == False:
                #print(NCBI_url)
                #print(file_BGC_ID,NCBI_url)
                try:
                    entrez_url_fasta(file_BGC_ID,NCBI_url)
                except:
                    continue
                t=random.randint(500,1000)*0.001
                time.sleep(t)
        pbar.update(1)
    pbar.close()

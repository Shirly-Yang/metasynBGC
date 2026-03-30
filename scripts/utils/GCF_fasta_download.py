import os
from BGC_NCBI_download  import entrez_url
from tqdm import tqdm
import random
import time

pathGCFfasta='GCF_fasta'
pathGCF='GCF_select_list'
pathmibig='mibig/fasta/'
pbar = tqdm(total=len(os.listdir(pathGCF)))
for i in os.listdir(pathGCF):
    print(i)
    #i='GCF_00414.txt'
    pathi=pathGCF+'/'+i
    patho=pathGCFfasta+'/'+i.replace('.txt','.fasta')
    if os.path.exists(patho) == False:
        filei=open(pathi,'r')
        fileo=open(patho,'w')
        linesi=filei.readlines()
        for l in linesi[1:]:
            BGC_ID=l.split('\t')[0]
            mibig= l.split('\t')[3]
            ncbi = l.split('\t')[4]
            if mibig != 'n/a':
                BGC_number=mibig.split('/')[-2]
                print('BGC_ID:',BGC_ID,'MiBig',BGC_number)
                if os.path.exists(pathmibig+BGC_number+'.fasta') == False:
                    continue
                filemibigfasta=open(pathmibig+BGC_number+'.fasta','r')
                BGCseq=filemibigfasta.readlines()[1]
            if ncbi != 'n/a':
                BGCseq=entrez_url(ncbi).split('\n')[1]
                t=random.randint(500,1000)*0.001 #设置一个随机的暂停时间，有些网站会把固定间隔的访问视作攻击，同时不暂停的访问容易被拉黑。生成1到3的随机数等待
                print(i,'BGC_ID:',BGC_ID,'NCBI delay',t,'s',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                time.sleep(t)   #等待一定的时间
            fileo.write('>'+BGC_ID+'\n'+BGCseq+'\n')
        fileo.close()
    pbar.update(1)
pbar.close()





import os
from tqdm import tqdm
from seqgrep import seqgrep


def panX_run(i,pathGCF,thread):
    i=i.split('.')[0]
    pathgbk=pathGCF+'/'+i+'/gbk'
    os.system("panX.py -fn %s -sl %s -t %s -dmi 50" % (pathgbk,i,thread))
    pathgbkinput=pathgbk+'/input_GenBank'
    count_bgc=len(os.listdir(pathgbk))
    if os.path.exists(pathgbkinput) == True:
        count_bgc=len(os.listdir(pathgbkinput))
    pathpanresult=pathgbk+'/protein_faa/diamond_matches/allclusters.tsv'
    pathreffaa=pathgbk+'/protein_faa/diamond_matches/reference.faa'
    fout=open(pathGCF+'/'+i+'/'+i+'_score_table.fasta','w')
    fileresult=open(pathpanresult,'r')
    linesresult=fileresult.readlines()
    n=0
    for l in linesresult:
        genomelist=[]
        n+=1
        genename=l.split('\t')[0].strip()
        for gene in l.split('\t'):
            genome=gene.split('|')[0]
            if genome not in genomelist:
                genomelist.append(genome)
        freq=str(float(len(genomelist)/float(count_bgc)))
        outnam=i+'_cluster'+str(n)+'_'+str(freq)
        print(genename,freq,len(genomelist),count_bgc)
        sequence=seqgrep(pathreffaa,genename)
        fout.write('>'+outnam+'\n'+sequence+'\n')
    fout.close()

#GCF_fold_root='GCF_select_fold'
#i='GCF_00012.txt'
#panX_run(i,GCF_fold_root)

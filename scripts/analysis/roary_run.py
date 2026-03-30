import os
from tqdm import tqdm
from seqgrep import seqgrep


def roary_run(i,pathGCF,thread):
    i=i.split('.')[0]
    pathgff=pathGCF+'/'+i+'/gff'
    pathresult=pathGCF+'/'+i+'/panresult'
    os.system("roary %s/*.gff -z -i 50 -s -f %s -p %s 2>&1" % (pathgff,pathresult,thread))
    if os.path.exists(pathgff) == True:
        count_bgc=len(os.listdir(pathgff))
    else:
        count_bgc=1
    pathpanresult=pathresult+'/clustered_proteins'
    pathreffaa=pathresult+'/_clustered'
    fout=open(pathGCF+'/'+i+'/'+i+'_score_table.fasta','w')
    fileresult=open(pathpanresult,'r')
    linesresult=fileresult.readlines()
    n=0
    for l in linesresult:
        genomelist=[]
        n+=1
        genelist=l.split(': ')[1].split('\t')
        genename=l.split(': ')[1].split('\t')[0].strip()
        for gene in genelist:
            genome=gene.split('_')[0]
            if genome not in genomelist:
                genomelist.append(genome)
        freq=float(len(genomelist)/float(count_bgc))
        freq=str(format(freq,'.5f'))
        outnam=i+'_cluster'+str(n)+'_'+str(freq)
        print(genename,freq,len(genomelist),count_bgc)
        sequence=seqgrep(pathreffaa,genename)
        fout.write('>'+outnam+'\n'+sequence+'\n')
    fout.close()
    fileresult.close()
#GCF_fold_root='GCF_select_fold'
#i='GCF_00429.txt'
#roary_run(i,GCF_fold_root,32)


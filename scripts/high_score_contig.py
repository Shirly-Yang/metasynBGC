import os
from tqdm import tqdm
from seqgrep import seqgrep


#pathGCF='GCF_select_fold'
#pathgenome='public_data/GEM/fna'
#i='GCF_08376.txt'

def high_score_contig(i,pathGCF,pathgenome,ratio,hits):
    hits=0
    i=i.split('.')[0]
    outnam=pathGCF+'/'+i+'/'+i+'_score_result.txt'
    high_ctg_path=pathGCF+'/'+i+'/'+i+'_high_contig'
    if os.path.exists(high_ctg_path) == False:
        os.system('mkdir %s' % (high_ctg_path))
    filei=open(outnam,'r')
    linesi=filei.readlines()
    min_score=float(linesi[0].split(': ')[-1].strip())*float(ratio)
    n=0
    for j in linesi[2:]:
        fnaname=j.split('\t')[0]
        score = float(j.split('\t')[1])
        if score < min_score or n>20:
            break
        filefna=pathgenome+'/'+fnaname
        fout=open(high_ctg_path+'/'+fnaname+'_high_score_contig.fasta','w')
        n+=1
        contig_list=j.split('\t')[2].rstrip(';').split(';')
        for contig in contig_list[:min(3,len(contig_list))]:
            #print(contig,contig_list[-1])
            if float(contig.split(' ')[1]) > hits:
                contigout=contig.split(' ')[0]
                contigseq=seqgrep(filefna,contigout)
                #print(fnaname,contigout)
                fout.write('>'+fnaname+'_'+contigout+'\n'+contigseq+'\n')
        fout.close()
    filei.close()   


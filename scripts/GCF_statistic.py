import os

pathgcf='/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM/GCF_select_fold'
fout=open('GCF_statistic.txt','w')
for i in os.listdir(pathgcf):
    pathfasta=os.path.join(pathgcf,i,'fasta')
    print(i,len(os.listdir(pathfasta)))
    fout.write(i+'\t'+str(len(os.listdir(pathfasta)))+'\n')
fout.close()

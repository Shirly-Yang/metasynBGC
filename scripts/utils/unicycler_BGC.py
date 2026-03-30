import os
import sys
from multiprocessing import Pool
thread=sys.argv[1]

filei=open('unicycler_23.8.31.txt','r')
linei=filei.readlines()

paralist=[]
for i in linei:
  
    #BGC='BGC0000413'
    #MAGs='3300013214_1.fna_high_score_contig.fasta'
    BGC=i.split('\t')[0]
    MAGs=i.split('\t')[1].strip()
    para=(MAGs,BGC)
    paralist.append(para)
    
    

    
def slidewindows(fastafile,fastafileout):
    fasta=open(fastafile,"r")
    fasta2=open(fastafileout,"w")
    lines=fasta.readlines()
    seq=""
    switch = 'on'
    for i in lines:
        
        if ">"  in i:
            switch = 'off'
            
            for m in range(int(((len(seq)-5000)/1000))+2):
                a=m*1000
                b=m*1000+5000
                fastam=seq[a:min(b,len(seq))]    
                fasta2.write(name+"_"+str(a)+"_"+str(min(b,len(seq)))+"\n"+fastam+'\n')
            name=i.replace("\n","")
            seq=""
        else:
            switch ='on'
        if switch == 'on':
            fastalinei=i.replace("\n","")          
            seq+=fastalinei
    for m in range(int(((len(seq)-5000)/1000))+2):
        a=m*1000
        b=m*1000+5000
        fastam=seq[a:min(b,len(seq))]    
        fasta2.write(name+"_"+str(a)+"_"+str(min(b,len(seq)))+"\n"+fastam+'\n')
    fasta2.close() 
    
def unicycler_run(para):
    MAGs=para[0]
    BGC=para[1]
    MAGs=MAGs.replace('_high_score_contig.fasta','')
    pathroot='/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM/unicycler/0831'
    pathmagsroot='/mnt/nfs/5110v5/wjc/metagenome_BGCs/public_data'
    #pathmagsroot='/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM/unicycler'

    if os.path.exists(pathroot) == False:
        os.system('mkdir %s' % (pathroot))
    pathbgc=os.path.join(pathroot,BGC)
    if os.path.exists(pathbgc) == False:
        os.system('mkdir %s' % (pathbgc))
    
    pathfasta=os.path.join('/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM/mibig/mibig_fasta',BGC+'.fasta')
    pathunic=os.path.join(pathroot,BGC)
    
    pathmags=os.path.join(pathmagsroot,MAGs)
    pathreads=os.path.join(pathunic,MAGs)
    
    if os.path.exists(pathreads+'_R1.fastq') == False: 
        print(pathreads,pathmags,pathreads)
        #os.system('iss generate --draft %s --output %s  --model hiseq --cpus %s -n 10M' % (pathmags,pathreads,thread))
        os.system('iss generate --draft %s --model hiseq --cpus %s -n 10M --output %s' % (pathmags,thread,pathreads.strip()))
        
    os.system('cp %s %s/bridge_tmp.fasta' % (pathfasta,pathunic))
    slidewindows(pathunic+"/bridge_tmp.fasta",pathunic+"/bridge.fasta")

    pathassembly=os.path.join(pathunic,MAGs+'_unicycler.fasta','assembly.fasta')
    if os.path.exists(pathassembly) == False:
        os.system('python /mnt/nfs/5110v5/wjc/Unicycler/unicycler-runner.py -1 %s/%s_R1.fastq -2 %s/%s_R2.fastq -l %s/bridge.fasta -t %s --mode bold -o %s_unicycler.fasta' % (pathunic,MAGs,pathunic,MAGs,pathunic,thread,pathunic+'/'+MAGs))
        os.system('cp %s %s' % (pathassembly,pathunic+'/'+MAGs+'_assembly.fasta'))
    
    os.system('antismash %s --genefinding-tool prodigal  --cb-knownclusters  --output-dir %s --cpus %s' % (pathunic+'/'+MAGs+'_assembly.fasta',pathunic+'/'+MAGs+'_BGC',thread))

    cp1=os.path.join('/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM/GCF_select_fold',BGC,BGC+'_BGC_result',MAGs+'_high_score_contig.fasta')
    cp2=pathunic+'/'+MAGs+'_BGC'+'/'+MAGs+'_high_score_contig.fasta'
    os.system('cp -r %s %s' % (cp1,cp2))
  

if __name__ == "__main__":
  pool=Pool(processes=1)
  pool.map(unicycler_run,paralist)
    #print(FAM,number)

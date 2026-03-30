import os
from tqdm import tqdm
#pathGCF='GCF_select_fold'
#i='GCF_08376'
#len(os.listdir(pathGCF))
#n=0
#for i in os.listdir(pathGCF)[:1]:
    #n+=1
def prokka_run(i,pathGCF,thread):
    #print(n,len(os.listdir(pathGCF)))
    i=i.split('.')[0]
    pathfasta=pathGCF+'/'+i+'/fasta'
    pathgbk=pathGCF+'/'+i+'/gbk'
    pathgff=pathGCF+'/'+i+'/gff'
    if os.path.exists(pathgbk) == False:
        os.system('mkdir %s' % (pathgbk))
    if os.path.exists(pathgff) == False:
        os.system('mkdir %s' % (pathgff))
    pbar = tqdm(total=len(os.listdir(pathfasta)))
    for j in os.listdir(pathfasta):
        pathj=pathfasta+'/'+j
        #print('pathj',pathj)
        os.system("prokka %s --outdir %s --cpus %s --quiet" % (pathj,pathj.split('.')[0],thread))
        pathresult=pathfasta+'/'+j.split('.')[0]+'/'
        for r in os.listdir(pathresult):
            if '.gbk' in r:
                filegbkin=pathresult+'/'+r
                filegbkout=pathgbk+'/'+j.split('.')[0]+'.gbk'       
                os.system('cp %s %s' % (filegbkin,filegbkout))
                #print('in',filegbkin,'out',filegbkout)
            if '.gff' in r:
                filegffin=pathresult+'/'+r
                filegffout=pathgff+'/'+j.split('.')[0]+'.gff'
                os.system('cp %s %s' % (filegffin,filegffout))
                #print('in',filegffin,'out',filegffout)

        pbar.update(1)
    pbar.close()


import os
from tqdm import tqdm
from multiprocessing import Pool

#pathgem='public_data/GEM/fna'
#pathGCF='GCF_select_fold'
#thread=60
#i='GCF_00061.txt'

def diamond_run(parameter):
    pathdb=parameter[0]
    pathgenome=parameter[1]
    result=parameter[2]
    command_dmd=''.join(['diamond blastx --db ',pathdb,' -q ',pathgenome,' --id 50 -p 1 -o ',result,' --salltitles  --quiet --more-sensitive --index-chunks 1 --block-size 1 ',' -t ./ '])
    os.system(command_dmd)
    pbar.update(thread)


def dmd_parameter_creat(i,pathGCF,pathgem,mibig_sum,mags_otu):
    i=i.split('.')[0]
    
    filemibig=open(mibig_sum,'r')
    filemags=open(mags_otu,'r')
    linemibig=filemibig.readlines()
    linemags=filemags.readlines()
    runlist=[]
    phylum='NA'
    for mibigl in linemibig:
        if i in mibigl:
            phylum=mibigl.split('\t')[0]
    if phylum == 'NA' or phylum == 'uncultured':
        runlist=os.listdir(pathgem)
    else:
        for magsl in linemags[1:]:
            if phylum == magsl.split(',')[1]:
                runlist.append(magsl.split(',')[0]+'.fna')
    filemibig.close()
    filemags.close()
    dmd_parameter=[]
    pathdmdresult=pathGCF+'/'+i+'/'+i+'_dmd_result'
    pathdmdBGCresult=pathGCF+'/'+i+'/'+i+'_dmdBGC_result'
    pathBGCfasta=pathGCF+'/'+i+'/fasta'
    if os.path.exists(pathdmdresult) == False:
        os.system('mkdir %s' % (pathdmdresult))
    if os.path.exists(pathdmdBGCresult) == False:
        os.system('mkdir %s' % (pathdmdBGCresult))
    print('diamond makedb')
    print(i)
    pathscore=pathGCF+'/'+i+'/'+i+'_score_table.fasta'
    pathdb=pathGCF+'/'+i+'/'+i+'_dmddb'
    logfile=pathGCF+'/'+i+'/'+i+'.log'
    command_dmddb=''.join(['diamond makedb --in ',pathscore,' --db ',pathdb,' -t ./ > ',logfile,' 2>&1'])
    os.system(command_dmddb)
    for BGC in os.listdir(pathBGCfasta):
        pathBGC=pathBGCfasta+'/'+BGC
        if '.fasta' in BGC and os.path.getsize(pathBGC) > 1000:
            result=pathdmdBGCresult+'/'+BGC+'.txt'
            para=(pathdb,pathBGC,result)
            dmd_parameter.append(para)
    for genome in runlist:
        pathgenome=pathgem+'/'+genome
        result=pathdmdresult+'/'+genome+'.txt'
        para=(pathdb,pathgenome,result)
        if os.path.exists(result) == False:
            dmd_parameter.append(para)
    return dmd_parameter

#pbar = tqdm(total=len(dmd_parameter))
#if __name__ == "__main__":
    #pool=Pool(processes=thread)
    #print(pool.map(diamond_run,dmd_parameter))
#pbar.close()

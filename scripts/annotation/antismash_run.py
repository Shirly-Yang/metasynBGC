import os

#pathGCF='GCF_select_fold'
#i='GCF_08376.txt'

def antismash_run(i,pathGCF,thread):
    i=i.split('.')[0]
    high_ctg_path=pathGCF+'/'+i+'/'+i+'_high_contig'
    antismash_path=pathGCF+'/'+i+'/'+i+'_BGC_result'
    if os.path.exists(antismash_path) == False:
        os.system('mkdir %s' % (antismash_path))
    print(high_ctg_path)
    for ctg in os.listdir(high_ctg_path):
        filein=high_ctg_path+'/'+ctg
        pathout=antismash_path+'/'+ctg
        print(filein,pathout)
        os.system('antismash %s --genefinding-tool prodigal  --cb-knownclusters  --output-dir %s --cpus %s' % (filein,pathout,thread))
        if os.path.exists(pathout) == True:
            gbk_count=0
            for f in os.listdir(pathout):
                if '.gbk' in f:
                    gbk_count+=1
            if gbk_count < 2:
                os.system('rm -R %s' % (pathout))



    


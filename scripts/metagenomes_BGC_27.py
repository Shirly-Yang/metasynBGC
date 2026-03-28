import os
from multiprocessing import Pool
from tqdm import tqdm
from NCBI_select_genbank_download import GCF_fasta_download
from collate_GCF import collate_GCF
from prokka_run import prokka_run
from seqgrep import seqgrep
from roary_run import roary_run
from diamond_run import dmd_parameter_creat
from score_computation import score_compute
from high_score_contig import high_score_contig
from antismash_run import antismash_run
import sys

pathNCBI_gbk='NCBI_selected_fasta'
pathmibig_gbk='mibig/fasta'
pathGCF_list='GCF_select_list'
GCF_fold_root='GCF_select_fold'
pathgenome='/mnt/nfs/5110v5/wjc/metagenome_BGCs/public_data'
mibig_sum='/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM/OTU/mibig_summary.txt'
mags_otu='/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM/OTU/OTU_OMD_GEM.csv'
#pathgenome='/mnt/nfs/5110v5/wjc/metagenome_BGCs/public_data/GEM/test'
BGC_select_ratio=0.6
contig_hits=3
thread=int(sys.argv[1])
#GCF=sys.argv[1]

def diamond_run(parameter):
    pathdb=parameter[0]
    pathgenome=parameter[1]
    result=parameter[2]
    command_dmd=''.join(['diamond blastx --db ',pathdb,' -q ',pathgenome,' --id 50 -p 1 -o ',result,' --salltitles  --quiet --more-sensitive --index-chunks 1 --block-size 1 ',' -t ./ '])
    os.system(command_dmd)
    pbar.update(thread)

#check and download BGC fasta file in GCF
#GCF_fasta_download(GCF,pathGCF_list,pathNCBI_gbk)

#copy BGC from GCF to GCF fold
#collate_GCF(GCF,pathNCBI_gbk,pathmibig_gbk,pathGCF_list,GCF_fold_root)

#annotation BGC, generate consistent formatted gbk file
#prokka_run(GCF,GCF_fold_root,thread)
filemibig=open(mibig_sum,'r')
linemibig=filemibig.readlines()
for GCF in linemibig[1005:1363]:
    GCF=GCF.split('\t')[1]
    if os.path.exists(GCF_fold_root+'/'+GCF) ==True and os.path.exists(GCF_fold_root+'/'+GCF+'/'+GCF+'_BGC_result') == False:
        #roary pan-genome analysis
        #print(len(os.listdir(GCF_fold_root+'/'+GCF+'/gff')),os.path.exists(GCF_fold_root+'/'+GCF+'/'+GCF+'_score_result.txt'),(GCF_fold_root+'/'+GCF+'/'+GCF+'_score_result.txt') )

        if len(os.listdir(GCF_fold_root+'/'+GCF+'/gff'))== 1:
            os.system("cp %s %s" % (GCF_fold_root+'/'+GCF+'/gff/*gff',GCF_fold_root+'/'+GCF+'/gff/'+GCF+'_copy.gff'))
            #print(GCF_fold_root+'/'+GCF+'/gff/'+GCF+'_copy.gff')
        roary_run(GCF,GCF_fold_root,thread)
        print(GCF)
        path_score_result=os.path.join("/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM/GCF_select_fold",GCF,GCF+"_score_result.txt")
        print(path_score_result)
        if os.path.exists(path_score_result) == False:
            print(path_score_result)
            #diamond
            dmd_parameter=dmd_parameter_creat(GCF,GCF_fold_root,pathgenome,mibig_sum,mags_otu)
            pbar = tqdm(total=len(dmd_parameter))
            pool=Pool(processes=thread)
            pool.map(diamond_run,dmd_parameter)
            pbar.close()

        #Calculate the score of GCF gene hits in each genome
        score_compute(GCF,GCF_fold_root)

        #Extract the contigs where the highest scoring BGCs are located
        high_score_contig(GCF,GCF_fold_root,pathgenome,BGC_select_ratio,contig_hits)

        #Run antismash in contigs where the highest scoring BGCs are located
        antismash_run(GCF,GCF_fold_root,thread)


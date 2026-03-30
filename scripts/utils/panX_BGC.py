import os
from multiprocessing import Pool
from tqdm import tqdm
from NCBI_select_genbank_download import GCF_fasta_download
from collate_GCF import collate_GCF
from prokka_run import prokka_run
from seqgrep import seqgrep
from panX_run import panX_run
from diamond_run import dmd_parameter_creat
from score_computation import score_compute
from high_score_contig import high_score_contig
from antismash_run import antismash_run
import sys

pathNCBI_gbk='NCBI_selected_fasta'
pathmibig_gbk='mibig/fasta'
pathGCF_list='GCF_select_list'
GCF_fold_root='GCF_select_fold'
pathgenome='/mnt/nfs/5110v5/wjc/metagenome_BGCs/public_data/GEM/fna'
BGC_top=20
contig_hits=3
thread=60
GCF=sys.argv[1]+'.txt'
cmd=sys.argv[2]

def diamond_run(parameter):
    pathdb=parameter[0]
    pathgenome=parameter[1]
    result=parameter[2]
    command_dmd=''.join(['diamond blastx --db ',pathdb,' -q ',pathgenome,' --id 50 -p 1 -o ',result,' --salltitles  --quiet --more-sensitive --index-chunks 1 --block-size 1 ',' -t ./ '])
    os.system(command_dmd)
    pbar.update(thread)

if cmd == 'prokka':
    #check and download BGC fasta file in GCF
    GCF_fasta_download(GCF,pathGCF_list,pathNCBI_gbk)

    #copy BGC from GCF to GCF fold
    collate_GCF(GCF,pathNCBI_gbk,pathmibig_gbk,pathGCF_list,GCF_fold_root)

    #annotation BGC, generate consistent formatted gbk file
    prokka_run(GCF,GCF_fold_root,thread)

if cmd == 'panX':
    #panX pan-genome analysis   other conda env (py2.7),This step is skipped for now and needs to be executed in another environment
    panX_run(GCF,GCF_fold_root,thread)

if cmd == 'antismash':
    #diamond
    dmd_parameter=dmd_parameter_creat(GCF,GCF_fold_root,pathgenome)
    pbar = tqdm(total=len(dmd_parameter))
    pool=Pool(processes=thread)
    pool.map(diamond_run,dmd_parameter)
    pbar.close()

    #Calculate the score of GCF gene hits in each genome
    score_compute(GCF,GCF_fold_root)

    #Extract the contigs where the highest scoring BGCs are located
    high_score_contig(GCF,GCF_fold_root,pathgenome,BGC_top,contig_hits)
    
    #Run antismash in contigs where the highest scoring BGCs are located
    antismash_run(GCF,GCF_fold_root,thread)


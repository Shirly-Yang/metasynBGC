from NCBI_select_genbank_download import GCF_fasta_download
import os

pathNCBI_gbk='NCBI_selected_fasta'
pathmibig_gbk='mibig/fasta'
pathGCF_list='GCF_select_list'
GCF_fold_root='GCF_select_fold'

n=0
for i in os.listdir(pathGCF_list):
    n+=1
    GCF=i
    m=len(os.listdir(pathGCF_list))
    print(n,'/',m)
    GCF_fasta_download(GCF,pathGCF_list,pathNCBI_gbk)


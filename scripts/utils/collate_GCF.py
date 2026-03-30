import os

#pathNCBI_gbk='NCBI_selected_fasta'
#pathmibig_gbk='mibig/fasta'
#pathGCF_list='GCF_select_list'
#GCF_fold_root='GCF_select_fold'

#for i in os.listdir(pathGCF_list)[0]:
    #i='GCF_08376.txt'
def collate_GCF(i,pathNCBI_gbk,pathmibig_gbk,pathGCF_list,GCF_fold_root):
    GCF=i.split('.')[0]
    GCF_fold=GCF_fold_root+'/'+GCF
    GCF_fold_gbk=GCF_fold+'/fasta'
    if os.path.exists(GCF_fold) == False:
        os.system('mkdir %s' % (GCF_fold))
    if os.path.exists(GCF_fold_gbk) == False:
        os.system('mkdir %s' % (GCF_fold_gbk))
    pathi=pathGCF_list+'/'+i
    filei=open(pathi,'r')
    linesi=filei.readlines()
    for l in linesi[1:]:
        BGC_ID=l.split('\t')[0]
        BGC_name=l.split('\t')[1].split('.')[0]
        if 'BGC' in BGC_name:
            gbkname=pathmibig_gbk+'/'+BGC_name+'.fasta'
        else:
            gbkname=pathNCBI_gbk+'/'+BGC_ID+'.fasta'
        #GCF_fold=GCF_fold_root+'/'+GCF
        #GCF_fold_gbk=GCF_fold+'/gbk/'
        #if os.path.exists(GCF_fold) == False:
            #os.system('mkdir %s & mkdir %s' % (GCF_fold,GCF_fold_gbk))
        gbkname_out=GCF_fold_gbk+'/'+BGC_ID+'.fasta'
        #print(gbkname_out)
        os.system('cp %s %s' % (gbkname,gbkname_out))

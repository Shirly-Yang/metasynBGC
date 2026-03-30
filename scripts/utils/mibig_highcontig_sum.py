import os

mibig_prokka='mibig/mibig_prokka'
def cds_mibig(BGC_gene):
    BGC=BGC_gene.split('_')[0]
    gene=int(BGC_gene.split('_')[1])
    pathmibigBGC=os.path.join(mibig_prokka,BGC)
    for i in os.listdir(pathmibigBGC):
        if '.gff' in i:
            cds=0
            pathgff=os.path.join(pathmibigBGC,i)
            filegff=open(pathgff,'r')
            linegff=filegff.readlines()
            for l in linegff:
                if '#' not in l and '\tID=PROKKA_' in l:
                    cds+=1
                if '##FASTA' in l:
                    break
    return(gene,(cds-gene+1)*(-1))


def cds_contig(BGC,MAG,gene):
    pathgff=os.path.join('GCF_select_fold',BGC,BGC+'_high_contig_analysis','gff',MAG+'_high_score_contig.gff')
    
    contig_gene={}
    filegff=open(pathgff,'r')
    linegff=filegff.readlines()
    for l in linegff:
        if '#' not in l and '\tID=PROKKA_' in l:
            contig=l.split('\t')[0]
            if contig not in contig_gene:
                contig_gene[contig]=0
            if contig in contig_gene:
                contig_gene[contig]+=1
        if '##FASTA' in l:
            break
    ctg_tmp=''
    n=0
    for l in linegff:
        if '#' not in l and '\tID=PROKKA_' in l:
            contig=l.split('\t')[0]
            if contig != ctg_tmp:
                ctg_tmp=contig
                n=0
            if contig == ctg_tmp:
                n+=1

        if gene in l:
            break
    return(n,(contig_gene[contig]-n+1)*(-1),ctg_tmp)

clustermibig='mibig/mibig_pan/result/clustered_proteins.txt'
filemibig=open(clustermibig,'r')
linemibig=filemibig.readlines()
GCF_fold_root='GCF_select_fold'
result_fold='highcontig_mibig_result'
for i in os.listdir(GCF_fold_root)[:]:
    #i='BGC0001089'
    highcontig=os.path.join(GCF_fold_root,i,i+'_high_contig')
    contiganalysis=os.path.join(GCF_fold_root,i,i+'_high_contig_analysis')
    contiggff=os.path.join(contiganalysis,'gff')
    dmdresult=os.path.join(contiganalysis,'dmdresult')
    if os.path.exists(dmdresult) == True:
        if len(os.listdir(dmdresult))>0:
            fout=open(os.path.join(result_fold,i+'_result.txt'),'w')
            for j in os.listdir(dmdresult):
                MAG=j.split('_high_score')[0]
                pathdmd=os.path.join(dmdresult,j)
                filedmd=open(pathdmd,'r')
                linesdmd=filedmd.readlines()
                dict_all={}
                noredu_BGC=[]
                for l in linesdmd:
                    ctg_gene=l.split('\t')[0]
                    mibig_gene=l.split('\t')[1]
                    identity=l.split('\t')[2]
                    #print(i,MAG,ctg_gene,cds_contig(i,MAG,ctg_gene),'\t',mibig_gene,cds_mibig(mibig_gene))
                    for clus in linemibig:
                        if mibig_gene in clus:
                            clus_list=clus.split('\t')[1:]
                            for g in clus_list:
                                BGC=g.split('_')[0]
                                if BGC not in noredu_BGC:
                                    noredu_BGC.append(BGC)
                                    dict_all[BGC]={}
                                if ctg_gene not in dict_all[BGC]:
                                    dict_all[BGC][ctg_gene]=[]
                                dict_all[BGC][ctg_gene].append((g.strip(),identity))
                sorted_dict = dict(sorted(dict_all.items(), key=lambda x: len(x[1]), reverse=True))
                n=0
                if i in sorted_dict:
                    BGC=i
                    if n <= 10:
                        #print(BGC,len(sorted_dict[BGC]),sorted_dict[BGC])
                        print(BGC,len(sorted_dict[BGC]))
                        fout.write(f'>>>{MAG}\t{BGC}\t{str(len(sorted_dict[BGC]))}\n')
                        for ctg_gene in sorted_dict[BGC]:
                            for hits in sorted_dict[BGC][ctg_gene]:
                                print(ctg_gene,cds_contig(i,MAG,ctg_gene),hits[0],cds_mibig(hits[0]))
                                fout.write(f'{MAG}\t{BGC}\t{ctg_gene}\t{str(cds_contig(i,MAG,ctg_gene)[2])},{str(cds_contig(i,MAG,ctg_gene)[0])},{str(cds_contig(i,MAG,ctg_gene)[1])}\t{hits[0]}\t{str(cds_mibig(hits[0])[0])},{str(cds_mibig(hits[0])[1])}\t{hits[1]}\n')
                        n+=1
            fout.close()

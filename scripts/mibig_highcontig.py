import os

dbmibig='mibig/mibig_pan/result/mibig_clustered'
GCF_fold_root='GCF_select_fold'
thread=30

for i in os.listdir(GCF_fold_root)[:]:
    #i='BGC0001089'
    highcontig=os.path.join(GCF_fold_root,i,i+'_high_contig')
    contiganalysis=os.path.join(GCF_fold_root,i,i+'_high_contig_analysis')
    contigprokka=os.path.join(contiganalysis,'prokka')
    contiggff=os.path.join(contiganalysis,'gff')
    contigpro=os.path.join(contiganalysis,'protein')
    dmdresult=os.path.join(contiganalysis,'dmdresult')
    if os.path.exists(contigprokka) == False:
        os.system('mkdir %s && mkdir %s && mkdir %s && mkdir %s && mkdir %s' % (contiganalysis,contigprokka,contiggff,contigpro,dmdresult))
    if os.path.exists(highcontig) == True:
        for j in os.listdir(highcontig):
            print(j)
            pathj=os.path.join(highcontig,j)
            prokkaj=os.path.join(contigprokka,j)
            if len(os.listdir(dmdresult))<=(len(os.listdir(highcontig))):
                os.system("prokka %s --outdir %s --cpus %s --centre c --force" % (pathj,prokkaj,thread))
                for f in os.listdir(prokkaj):
                    if '.faa' in f:
                        proin=os.path.join(prokkaj,f)
                    if '.gff' in f:
                        gffin=os.path.join(prokkaj,f)
                proout=os.path.join(contigpro,j.replace('.fasta','.faa'))
                gffout=os.path.join(contiggff,j.replace('.fasta','.gff'))
                dmdout=os.path.join(dmdresult,j.replace('.fasta','_dmd.txt'))
                os.system('cp %s %s && cp %s %s' % (proin,proout,gffin,gffout))
                os.system('diamond blastp --db %s -q %s -o %s --id 30 --salltitles  --quiet --more-sensitive --index-chunks 1 --block-size 1' % (dbmibig,proout,dmdout))





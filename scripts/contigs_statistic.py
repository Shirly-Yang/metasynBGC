import os
pathroot='/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM/GCF_select_fold'
fileo=open('/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM/contigs_statistic.txt','w')
for i in os.listdir(pathroot):
	pathbgc=os.path.join(pathroot,i)
	pathcontig=os.path.join(pathbgc,i+'_high_contig')
	if os.path.exists(pathcontig):
		for z in os.listdir(pathcontig):
			filez=open(os.path.join(pathcontig,z),'r')
			for lines in filez.readlines():
				if '>' in lines:
					fileo.write(i+'\t'+z+'\t'+lines)
					print(i)
			
fileo.close()
		
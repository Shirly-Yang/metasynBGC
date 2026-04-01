import os
pathroot='/path/to/BIGFAM/GCF_select_fold'
fileo=open('/path/to/BIGFAM/contigs_statistic.txt','w')
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
		

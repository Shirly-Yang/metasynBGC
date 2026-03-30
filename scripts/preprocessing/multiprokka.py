from multiprocessing import Pool
import os

filefasta=[]
pathi='/path/to/BIGFAM/mibig/mibig_fasta'
pathresult='/path/to/BIGFAM/mibig/mibig_prokka'
m=0
n=0
for i in os.listdir(pathi):
    m+=1
    pathii=pathi+'/'+i
    pathresulti=pathresult+'/'+i.split('.')[0]
    inout=(pathii,pathresulti)
    if os.path.exists(pathresulti)==False:
      filefasta.append(inout)
      n+=1
      print(i,n,m)
    else:
      if len(os.listdir(pathresulti)) < 11:
        filefasta.append(inout)
        os.system('rm -r %s' % (pathresulti))
        n+=1
        print(i,n,m)

def multirun(parameter):
    pathi=parameter[0]
    patho=parameter[1]
    os.system("prokka %s --cpus 1 --outdir %s" % (pathi,patho))
    #print(parameter)

if __name__ == "__main__":
    pool=Pool(processes=60)
    pool.map(multirun,filefasta)


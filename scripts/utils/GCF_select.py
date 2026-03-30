import os
from tqdm import tqdm

pathall='GCF_list'
pathselect='GCF_select_list'
if os.path.exists(pathselect) == False:
    os.system('mkdir %s' % (pathselect))

pbar = tqdm(total=len(os.listdir(pathall)))

n=0

for i in os.listdir(pathall):
    pathi=pathall+'/'+i
    patho=pathselect+'/'+i
    print(patho)
    filei=open(pathi,'r')
    linesi=filei.readlines()
    for l in linesi[1:]:
        mibig=l.split('\t')[3]
        if mibig != 'n/a':
            os.system('cp %s %s' % (pathi,patho))
            print('cp to',patho)
            n+=1
            break
        
    pbar.update(1)
print(n)
pbar.close()

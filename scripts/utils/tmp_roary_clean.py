import os

def clean_tmp(pathrun,pathmv):
    if os.path.exists(pathmv) == False:
        os.system('mkdir %s' % (pathmv))
    for i in os.listdir(pathrun):
        pathi=pathrun+'/'+i
        clean='F'
        if os.path.isdir(pathi)==True:
            try:
                for j in os.listdir(pathi):
                    #print(j,'.proteome.faa' not in j)
                    if '.proteome.faa' not in j:
                        break
                    clean='T'
                #print(clean)
                if clean == 'T':
                    patho=pathmv+'/'+i
                    os.system('mv %s %s' % (pathi,patho))
                    print(pathi,patho)
            except OSError as e:
                continue

clean_tmp('/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM','/mnt/nfs/5110v5/wjc/metagenome_BGCs/BIGFAM/tmp')

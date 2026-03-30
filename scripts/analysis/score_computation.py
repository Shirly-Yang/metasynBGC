import os
from tqdm import tqdm

def freq2score(freq):
    score=3**float(freq)-1
    return score

def max_BGC_len(GCF):
    pathfasta='GCF_select_fold/'+GCF+'/fasta'
    lenlist=[]
    for i in os.listdir(pathfasta):
        if '.fasta' in i:
            pathi=pathfasta+'/'+i
            filei=open(pathi,'r')
            lenlist.append(len(filei.readlines()[1]))
            filei.close()
    maxlen=max(lenlist)
    return maxlen

def compute(hitslist,maxlen):
    total_score=0
    cluster_score={}
    contig_count={}
    for i in hitslist:
        ctgi=i[0]

        positioni=i[1]
        clusteri=i[2]
        freqi=float(i[3])
        multiple=1
        for j in hitslist:
            ctgj=j[0]
            positionj=j[1]
            clusterj=j[2]
            if ctgi==ctgj and abs(positioni-positionj)<maxlen and clusteri != clusterj:
                multiple+=1
        multiple=min(multiple,10)
        score_clusteri=multiple*(freq2score(freqi))
        if ctgi in contig_count:
            contig_count[ctgi]+=score_clusteri
        else:
            contig_count[ctgi]=score_clusteri
        
        if clusteri in cluster_score:
            cluster_score[clusteri]=max(cluster_score[clusteri],score_clusteri)
        else:
            cluster_score[clusteri]=score_clusteri
    cluster_score_str=''
    cluster_score_sort=sorted(cluster_score.items(),key = lambda x:x[1],reverse = True)
    cluster_score_sort=dict(cluster_score_sort)
    for clusterkey in cluster_score_sort:
        #print(i,clusterkey)
        #print(cluster_score[clusterkey])
        total_score+=cluster_score[clusterkey]
        cluster_score_str+=clusterkey
        cluster_score_str+=' '
        cluster_score_str+=str(cluster_score[clusterkey])
        cluster_score_str+=';'
    contig_count_str=''
    contig_count_sort=sorted(contig_count.items(),key = lambda x:x[1],reverse = True)
    contig_count_sort=dict(contig_count_sort)
    for contig in contig_count_sort:
        contig_count_str+=contig
        contig_count_str+=' '
        contig_count_str+=str(contig_count[contig])
        contig_count_str+=';'
    return total_score,cluster_score_str,contig_count_str

#pathGCF_list='GCF_select_list'
#pathGCF='GCF_select_fold'
#i='GCF_000061.txt'
#for i in os.listdir(pathGCF_list)[:1]:
def score_compute(i,pathGCF):
    i=i.split('.')[0]
    pathdmdresult=pathGCF+'/'+i+'/'+i+'_dmd_result'
    pathdmdBGCresult=pathGCF+'/'+i+'/'+i+'_dmdBGC_result'
    outnam=pathGCF+'/'+i+'/'+i+'_score_result.txt'
    fout=open(outnam,'w')
    maxlen=max_BGC_len(i)
    #print(i,maxlen,len(os.listdir(pathdmdresult)))
    pbar = tqdm(total=len(os.listdir(pathdmdresult)))
    outputlist={}
    BGC_max_score=0
    BGC_max=''
    BGC_min_score=99999999
    BGC_min=''
    for j in os.listdir(pathdmdBGCresult):
        hitslist=[]
        #print(j)
        filej=open(pathdmdBGCresult+'/'+j,'r')
        linesj=filej.readlines()
        pbar.update(1)
        for l in linesj:
            ctg=l.split('\t')[0]
            position=(int(l.split('\t')[6])+int(l.split('\t')[7]))/2
            cluster=l.split('\t')[1].split('_')[-2]
            freq=float(l.split('\t')[1].split('_')[-1])
            hit=(ctg,position,cluster,freq)
            hitslist.append(hit)
            #print(i,ctg,position,cluster,freq)
        if compute(hitslist,maxlen)[0] < BGC_min_score:
            BGC_min_score = compute(hitslist,maxlen)[0]
            BGC_min = j.split('.txt')[0]
        if compute(hitslist,maxlen)[0] > BGC_max_score:
            BGC_max_score = compute(hitslist,maxlen)[0]
            BGC_max = j.split('.txt')[0]
        filej.close()
    fout.write('#The maximum score BGC in '+i+' is '+BGC_max+' : '+str(BGC_max_score)+'. Minimum score BGC is '+BGC_min+' : '+str(BGC_min_score)+'\n')
    fout.write('Genome\tTotal Score\tContig Score\tCluster Score\n')
    for j in os.listdir(pathdmdresult):
        hitslist=[]
        #print(j)
        filej=open(pathdmdresult+'/'+j,'r')
        linesj=filej.readlines()
        pbar.update(1)
        for l in linesj:
            ctg=l.split('\t')[0]
            position=(int(l.split('\t')[6])+int(l.split('\t')[7]))/2
            cluster=l.split('\t')[1].split('_')[-2]
            freq=float(l.split('\t')[1].split('_')[-1])
            hit=(ctg,position,cluster,freq)
            hitslist.append(hit)
            #print(i,ctg,position,cluster,freq)
        outcontent=str(j.split('.txt')[0]+'\t'+str(compute(hitslist,maxlen)[0])+'\t'+str(compute(hitslist,maxlen)[2])+'\t'+str(compute(hitslist,maxlen)[1])+'\n')
        outputlist[outcontent]=compute(hitslist,maxlen)[0]
        filej.close()
    outputlist_sort=sorted(outputlist.items(),key = lambda x:x[1],reverse = True)
    for output in outputlist_sort:
        #print(output)
        fout.write(output[0])
    pbar.close()
    fout.close()


#pathGCF_list='GCF_select_list'
#pathGCF='GCF_select_fold'
#i='GCF_00429.txt'
#score_compute(i,pathGCF)

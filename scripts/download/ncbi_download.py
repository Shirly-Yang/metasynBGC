
from Bio import Entrez
from tqdm import tqdm
import time
import random
Entrez.email = 'zokla@foxmail.com'

def entrez_url(filenam,url):

    genome_id = url.split('/')[-1].split('?')[0]
    seq_start = url.split('from=')[-1].split('&to')[0]
    seq_stop = url.split('to=')[-1].split("'")[0]
    #print(seq_start,seq_stop)
    search_results = Entrez.read(
        Entrez.esearch(
            db="nucleotide", term=genome_id, restart=0, retmax=100000
        )
    )
    count = int(search_results["Count"])
    id_list = search_results["IdList"]

    fetch_handle = Entrez.efetch(
        db="nucleotide", id=id_list, rettype="genbank", retmode="text",
        seq_start=seq_start, seq_stop=seq_stop
    )
    data = fetch_handle.read()
    fetch_handle.close()
    #data = data[:data.find('\n')] + '\n' + data[data.find('\n'):].replace('\n', '') + '\n'
    fout=open(filenam,'w')
    fout.write(data)
    fout.close()


def entrez_url_fasta(filenam,url):

    genome_id = url.split('/')[-1].split('?')[0]
    seq_start = url.split('from=')[-1].split('&to')[0]
    seq_stop = url.split('to=')[-1].split("'")[0]
    #print(seq_start,seq_stop)
    search_results = Entrez.read(
        Entrez.esearch(
            db="nucleotide", term=genome_id, restart=0, retmax=100000
        )
    )
    count = int(search_results["Count"])
    id_list = search_results["IdList"]

    fetch_handle = Entrez.efetch(
        db="nucleotide", id=id_list, rettype="fasta", retmode="text",
        seq_start=seq_start, seq_stop=seq_stop
    )
    data = fetch_handle.read()
    fetch_handle.close()
    #data = data[:data.find('\n')] + '\n' + data[data.find('\n'):].replace('\n', '') + '\n'
    data = data[data.find('\n'):].replace('\n', '') + '\n'
    fout=open(filenam,'w')
    fout.write('>'+filenam.split('.')[0].split('/')[1]+'\n'+data)
    fout.close()

#filenam='NCBI_selected_gbk/test.txt'
#url='https://www.ncbi.nlm.nih.gov/nuccore/NHZS01000286.1?from=28390&to=69461'

#entrez_url(filenam,url)


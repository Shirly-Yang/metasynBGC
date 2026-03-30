def seqgrep(pathfasta,genenam):
    filefasta=open(pathfasta,'r')
    linesfasta=filefasta.readlines()
    seq=''
    switch=0
    for l in linesfasta:
        if '>' in l:
            switch =0
        if switch == 1:
            seq+=l.strip()
        if '>' in l and genenam in l:
            switch = 1
    filefasta.close()
    return seq

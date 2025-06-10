# -*- coding: utf-8 -*-

## usage: python2 allele_cali.one_chr.py <filename> <reference genome> <output>
## <filename>: .vcf.gz file input, full name
## <reference genome>: chr${chr}.fa.gz
## <output>: .vcf.gz file output, full name

import sys
import gzip
import os
import re
import itertools
import pandas
import gc

###############################
##########   check   ##########
###############################
filename = sys.argv[1]
if os.path.isfile(filename):
    print('Input .vcf.gz file found.')
else:
    print(filename+' not found, pls check your filename.')
    print('Usage: python '+str(sys.argv[0])+' <filename> <reference genome> <output>')
    exit()

genome = sys.argv[2]
if os.path.isfile(genome):
    print('Input reference genome file found.')
else:
    print(genome+' not found, pls check your path for ancestor genome.')
    print('Usage: python '+str(sys.argv[0])+' <filename> <reference genome> <output>')
    exit()

output = sys.argv[3]


################################
##########   genome   ##########
################################
print('Reading reference genome...')

human_ancestror_genome = ['']
with gzip.open(genome,'r') as f:
    #pattern  = re.compile(r'[\d\w]+') ## to extract the chromosome ID
    line = f.readline()
    line = f.readline()
    while line:
        human_ancestror_genome += line.strip().upper()
        line = f.readline()
print('Reference genome ready.')

## convert list to dict
human_ancestror_genome = dict(itertools.izip(xrange(len(human_ancestror_genome)),human_ancestror_genome))

##################################
##########   vcf file   ##########
##################################
replacedict = {'1|1':'0|0','0|0':'1|1','0|1':'1|0','1|0':'0|1', '1|.':'0|.','0|.':'1|.','.|1':'.|0','.|0':'.|1','.|.':'.|.', '1/1':'0/0','0/0':'1/1','0/1':'1/0','1/0':'0/1', '1/.':'0/.','0/.':'1/.','./1':'./0','./0':'./1','./.':'./.', "0":"1","1":"0"}

# '1|1':'0|0','0|0':'1|1','0|1':'1|0','1|0':'0|1'
# '1|.':'0|.','0|.':'1|.','.|1':'.|0','.|0':'.|1','.|.':'.|.'

# '1/1':'0/0','0/0':'1/1','0/1':'1/0','1/0':'0/1'
# '1/.':'0/.','0/.':'1/.','./1':'./0','./0':'./1','./.':'./.' 

# "0":"1","1":"0"

with gzip.open(output[:-3]+'.mismatch.gz','w') as log:
    pass
log = gzip.open(output[:-3]+'.mismatch.gz','a')

with gzip.open(filename) as fin:
    with gzip.open(output,"w") as fout:
        line = fin.readline()
        while line:
            if line[0] == "#":
                fout.write(line)
            else:
                tmp = line.strip().split("\t")
                chromo, pos, rsid, ref, alt, qual, filt, info, foma = tmp[:9]
                if (len(ref) != 1) or (len(alt) != 1):
                    log.write(str(chromo)+"\t"+str(pos)+"\t"+rsid+"\t"+ref+"\t"+alt+"\n")
                else:
                    if human_ancestror_genome[int(pos)] == ref:
                        fout.write(line)
                    elif human_ancestror_genome[int(pos)] == alt:
                        geno = tmp[9:]
                        newgeno = '\t'.join([replacedict.get(g,g) for g in geno])
                        fout.write(str(chromo)+"\t"+str(pos)+"\t"+rsid+"\t"+alt+"\t"+ref+"\t"+qual+"\t"+filt+"\t"+info+"\t"+foma+"\t"+newgeno+"\n")
                    else:
                        log.write(str(chromo)+"\t"+str(pos)+"\t"+rsid+"\t"+ref+"\t"+alt+"\n")

            line = fin.readline()

log.close()

print('Done.')
print('Have a Nice Day!')

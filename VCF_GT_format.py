## to remain only the "GT" field in the VCF file
## usage: python2 VCF_GT_format.py <input.vcf.gz> | bgzip -c > <output.vcf.gz> 

import gzip
import os
import sys

inp = sys.argv[1]

with gzip.open(inp) as f:
    line = f.readline()
    while line:
        if line[0] == '#':
            print(line.strip())
            
            line = f.readline()
        else:
            while line:
                infos = line.strip().split('\t')
                #infos[2] = '{}:{}:{}:{}'.format(infos[0],infos[1],infos[3],infos[4])
                infos[8] = 'GT'
                genos = [x.split(':')[0] for x in infos[9:]]
                infos = infos[:9] + genos
                print('\t'.join(infos))

                line = f.readline()


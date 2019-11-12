#Email:fanyucai1@126.com
#2019.7.8

import os
import argparse
import subprocess
import json
fastp="/software/fastp/fastp"
def run(pe1,pe2,minlen,prefix,outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    outdir=os.path.abspath(outdir)
    pe1=os.path.abspath(pe1)
    pe2=os.path.abspath(pe2)
    os.chdir(outdir)
    par=" --detect_adapter_for_pe -W 4 -M 20 -l %s -w 8 -j %s.json -h %s.html " %(minlen,prefix,prefix)
    cmd="%s -i %s -I %s -o %s.R1.fq.gz -O %s.R2.fq.gz %s " %(fastp,pe1,pe2,prefix,prefix,par)
    subprocess.check_call(cmd, shell=True)
    json_file= os.path.abspath("%s/%s.json"%(outdir,prefix))
    outfile = open("%s/%s.csv" % (outdir, prefix), "w")
    outfile.write("SampleID\tRaw_reads\tRaw_bases\tRaw_q30_rate\tGC_content"
                  "\tClean_reads\tClean_bases\n")
    with open("%s" % (json_file), "r") as load_f:
        load_dict = json.load(load_f)
        raw1 = load_dict['summary']['before_filtering']["total_reads"]
        raw2 = load_dict['summary']['before_filtering']['total_bases']
        raw3=load_dict['summary']['before_filtering']['q30_rate']
        raw4=load_dict['summary']['before_filtering']['gc_content']
        clean1 = load_dict['summary']['after_filtering']["total_reads"]
        clean2 = load_dict['summary']['after_filtering']['total_bases']
    outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (prefix, raw1, raw2, raw3,raw4,clean1,clean2))
    outfile.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser("QC using fastp.")
    parser.add_argument("-p1", "--pe1", help="5 reads", required=True)
    parser.add_argument("-p2", "--pe2", help="3 reads", required=True)
    parser.add_argument("-o", "--outdir", help="output directory", default=os.getcwd())
    parser.add_argument("-p", "--prefix", help="prefix of output", default="out.clean")
    parser.add_argument("-l","--minlen",help="min length output default is 75",default=75)
    args = parser.parse_args()
    run(args.pe1,args.pe2,args.minlen,args.prefix,args.outdir)

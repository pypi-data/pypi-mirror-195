"""
Converts the 5' and 3' coordinates of reads into coordinates on meta-features.
In essence, each feature is divided into bins; the 5' and 3' coordinates of
each read contained in each feature are replaced by the bin index in which
they are included. For example for a feature of length 100 containing a read
with coordinates [5', 3']: [15, 95] the corresponding meta-coordinates for
10 bins are [1, 9]. THe script works only for +ve strands and BED coordinates
grater than certain length of nucleotide set in 'min-len' parameter.
"""

import sys
import pysam
import argparse

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--ifile",
                    help="Input SAM/BAM file")
    parser.add_argument("-b", "--bed",
                    help="Bed file with gene feature coordinates")
    parser.add_argument("-f", "--sam", action='store_true',
                    help="Use this option if input file SAM")
    parser.add_argument("-c", "--bins", default=20, type=int,
                    help="Number of bins, per feature, default: %(default)s" )
    parser.add_argument("-l", "--min-len", default=200, type=int,
                    help="Minimum transcript length processed, default:%(default)s")
    parser.add_argument("-d", "--col-qname-name", default="qname",
                    help="Header for column query name, default: qname")
    parser.add_argument("-e", "--col-feat-name", default="feat",
                    help="Header of column wih features, default: feat")
    parser.add_argument("-g", "--col-bin5p-name", default="bin5p",
                    help="Header for 5 prime bins of read, default: bin5p")
    parser.add_argument("-j", "--col-bin3p-name", default="bin3p",
                    help="Header for 3 prime bins of read, default: bin3p")
    parser.add_argument("-s", "--col_delimiter", default="\t",
                    help="Delimiter of output file columns, default: tab(\t)")
    args = parser.parse_args()

    filemode = "rb"
    if args.sam:
        filemode = "r"

    region_coords = {}
    with open(args.bed) as bedfile:
        for line in bedfile:
            line = line.strip().split("\t")
            if line[5] == "-":
                print("Error: Code does not support calculations for -ve strand")
                sys.exit(1)
            refid = line[0]
            ref_start = int(line[1])
            ref_end = int(line[2])
            if (ref_end - ref_start) < args.min_len:
                continue
            if refid in region_coords:
                print("Error: Dulplicate transcripts found ")
                sys.exit(1)
            region_coords[refid] = [ref_start, ref_end]

    delim = args.col_delimiter
    print(delim.join([args.col_qname_name, args.col_feat_name, args.col_bin5p_name, args.col_bin3p_name]))

    infile = pysam.AlignmentFile(args.ifile, filemode)
    for read in infile:
        if read.is_unmapped or read.is_reverse: #check for unmapped and -ve strand
            continue
        qname = read.query_name
        refname = read.reference_name
        qstart = read.reference_start
        qstop = read.reference_end - 1

        if refname in region_coords:
            bed_start = region_coords[refname][0]
            bed_end = region_coords[refname][1]

            bin_len = (bed_end - bed_start)/args.bins
            bin5p = int((qstart - bed_start)/bin_len)
            bin3p = int((qstop - bed_start)/bin_len)

            if bin5p < 0 or bin5p >= args.bins:
                bin5p = "NA"

            if bin3p < 0 or bin3p >= args.bins:
                bin3p = "NA"
            print(delim.join([qname, refname, str(bin5p), str(bin3p)]))

from adjust_date import adjust_date

def stat(afile,acontext):
	fp = open(afile,"r")
	for line in fp:
		aa = line.strip().split(";")
		bb,cc = adjust_date(aa[1],aa[2])
		print acontext + ";" + aa[0] + ";" + str(bb) + ";" + str(cc)
	fp.close()

def main(args):
    if args.file is not None and args.context is not None:
        stat(args.file,args.context)
    else:
        print("You must set a file and a context!")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='time_stat.py',
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f','--file',
            required=True,
            help="-f stat.txt.uniq.csv\t : Set the message file.")
    parser.add_argument('-c','--context',
            required=True,
            help="-c stat\t : Set the context string.")
    args = parser.parse_args()
    main(args)

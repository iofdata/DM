import hashlib

def md5(data_str):
    """#data_str="com.peony.monitor.analysis.AnalysisMonitorTask"""
    md5=hashlib.md5(data_str.encode("utf-8")).hexdigest()
    print(md5)

def main(args):
    if args.string is not None:
        md5(args.string)
    else:
        print("You must set a string!")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='md5.py',
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-s','--string',
            required=True,
            help="-s ES.monitor.ESConnectionMonitor\t : Set the class string to check it MD5.")
    args = parser.parse_args()
    main(args)

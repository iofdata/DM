# -*- coding: utf-8 -*-
#encoding=UTF-8

"""	
	@File:   ParserExcel.py   
	@Author: Hao Tan
	@Date:   2014-12-18 
	@Email:  tanhao2013@foxmail.com
	@Desc:   A short script for parsering excel file into a json|dict config file.
"""


from xlrd import open_workbook,empty_cell
import json

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class PaserExcel():
    def __init__(self, xls):
        self.xls = xls
        self.data = {}

    def PaserSheet(self):
        try:
            wb = open_workbook(self.xls)
            for s in wb.sheets():
                self.data[s.name] = PaserTable(s)
        except Exception, e:
            print(str(e))

def PaserTable(s):
    result = {}
    if s.cell_type(0,0):
        for row in range(1,s.nrows):
            rname = s.cell(row,0).value
            celldata = s.cell(row,1)
            if not (celldata is empty_cell):
                result[rname.decode("utf-8")] = celldata.value
    else:
        from collections import defaultdict
        result = defaultdict(dict)
        for col in range(1,s.ncols):
            for row in range(1,s.nrows):
                rname = s.cell(row,0).value
                cname = s.cell(0,col).value
                if str(cname).decode('utf8') == u'性能型':
                    cname = 1
                if str(cname).decode('utf8') == u'容量型':
                    cname = 0
                celldata = s.cell(row,col)
                if celldata.value:
                    result[str(cname)][str(rname)] = celldata.value
    return result

def main(args):
    tmp = PaserExcel(args.file)
    tmp.PaserSheet()
    #print(json.dumps(tmp.data,indent=4))
    for item in tmp.data:
        print str(item) + " = " + str(json.dumps((tmp.data)[item],indent=4))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='ParserExcel.py',
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f','--file',
            required=True,
            help="-f price.xls : the price xls tables!")
    args = parser.parse_args()
    main(args)

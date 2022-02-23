# -*- coding: utf-8

import argparse
import os
import sys

from . import n2d
from . import d2n
from . import n2q
from . import q2n
from . import n2o
from . import o2n

def convertSentences(inputText) :
	if args.n2d :
		return n2d.ND(inputText, args.det)

	elif args.d2n :
		return d2n.DN(inputText, args.det)

	elif args.n2q :
		return n2q.NQ(inputText, args.det)

	elif args.q2n :
		return q2n.QN(inputText, args.det)

	elif args.n2o :
		return n2o.NO(inputText, args.det)

	elif args.o2n :
		return o2n.ON(inputText, args.det)

	else :
		sys.exit(0)

# コマンドライン引数の解析
parser = argparse.ArgumentParser()

parser.add_argument("-n2d", action = "store_true")
parser.add_argument("-d2n", action = "store_true")
parser.add_argument("-n2q", action = "store_true")
parser.add_argument("-q2n", action = "store_true")
parser.add_argument("-n2o", action = "store_true")
parser.add_argument("-o2n", action = "store_true")
parser.add_argument("-det", action = "store_true")
parser.add_argument("-cur", action = "store_true")
parser.add_argument("-file", action = "store_true")

args = parser.parse_args()

# 手動
if args.cur :
	print("「e」か「え」を入力で終了")
	print("")
	while True :
		print("---------------------------------------------")

		print("input  : ", end = "")
		inputText = input()
		if inputText == 'e' or inputText == 'え' :
			break

		print("output : " + convertSentences(inputText).strip())

# ファイル入出力
elif args.file :
	print("input file  : ", end = "")
	iFile = input()
	print("output file : ", end = "")
	oFile = input()

	with open(iFile, "r") as r :
		with open(oFile, "w") as w :
			for line in r :
				w.write(str(convertSentences(line.strip())))

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
		return n2d.ND(inputText, args.detail)

	elif args.d2n :
		return d2n.DN(inputText, args.detail)

	elif args.n2q :
		return n2q.NQ(inputText, args.detail)

	elif args.q2n :
		return q2n.QN(inputText, args.detail)

	elif args.n2o :
		return n2o.NO(inputText, args.detail)

	elif args.o2n :
		return o2n.ON(inputText, args.detail)

	else :
		sys.exit(0)

# コマンドライン引数の解析
parser = argparse.ArgumentParser(description = "変換のオプション指定には、n2oやd2nのように、変換元か変換先のどちらかに平叙文肯定(n)を含む必要があります。こちらも併せてご覧下さい(https://pypi.org/project/csw/)。")

parser.add_argument("--n2d", action = "store_true", help = "平叙文肯定から平叙文否定への変換")
parser.add_argument("--d2n", action = "store_true", help = "平叙文否定から平叙文肯定への変換")
parser.add_argument("--n2q", action = "store_true", help = "平叙文肯定から疑問文への変換")
parser.add_argument("--q2n", action = "store_true", help = "疑問文から平叙文肯定への変換")
parser.add_argument("--n2o", action = "store_true", help = "平叙文肯定から命令文への変換")
parser.add_argument("--o2n", action = "store_true", help = "命令文から平叙文肯定への変換")
parser.add_argument("-d", "--detail", action = "store_true", help = "形態素解析の結果を表示(fオプションとの併用不可)")
parser.add_argument("-c", "--current", action = "store_true", help = "一文ずつ入出力(fオプションとの併用不可)")
parser.add_argument("-f", "--file", nargs = 2, help = "ファイルでの入出力(その後ろに変換元ファイル名、変換先ファイル名を順に指定)")

args = parser.parse_args()

# 手動
if args.current :
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
	iFile = args.file[0]
	oFile = args.file[1]

	with open(iFile, "r") as r :
		with open(oFile, "w") as w :
			for line in r :
				w.write(str(convertSentences(line.strip())))

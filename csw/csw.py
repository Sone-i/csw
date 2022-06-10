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
from . import spj
from . import kk

def cn2d(inputText) :
	return n2d.ND(inputText, args.detail)
def cn2q(inputText) :
	return n2q.NQ(inputText, args.detail)
def cn2o(inputText) :
	return n2o.NO(inputText, args.detail)

def cd2n(inputText) :
	return d2n.DN(inputText, args.detail)
def cd2q(inputText) :
	return n2q.NQ(d2n.DN(inputText, args.detail).strip(), args.detail)
def cd2o(inputText) :
	return n2o.NO(d2n.DN(inputText, args.detail).strip(), args.detail)

def cq2n(inputText) :
	return q2n.QN(inputText, args.detail)
def cq2d(inputText) :
	return n2d.ND(q2n.QN(inputText, args.detail).strip(), args.detail)
def cq2o(inputText) :
	return n2o.NO(q2n.QN(inputText, args.detail).strip(), args.detail)

def co2n(inputText) :
	return o2n.ON(inputText, args.detail)
def co2d(inputText) :
	return n2d.ND(o2n.ON(inputText, args.detail).strip(), args.detail)
def co2q(inputText) :
	return n2q.NQ(o2n.ON(inputText, args.detail).strip(), args.detail)

def convertSentences(inputText) :
	if args.n2d :
		return cn2d(inputText)
	elif args.n2q :
		return cn2q(inputText)
	elif args.n2o :
		return cn2o(inputText)

	elif args.d2n :
		return cd2n(inputText)
	elif args.d2q :
		return cd2q(inputText)
	elif args.d2o :
		return cd2o(inputText)

	elif args.q2n :
		return cq2n(inputText)
	elif args.q2d :
		return cq2d(inputText)
	elif args.q2o :
		return cq2o(inputText)

	elif args.o2n :
		return co2n(inputText)
	elif args.o2d :
		return co2d(inputText)
	elif args.o2q :
		return co2q(inputText)

	elif args.n :
		mode = spj.SPJ(inputText)
		if mode == "n" :
			return kk.myParse(inputText, args.detail)
		elif mode == "d" :
			return cd2n(inputText)
		elif mode == "q" :
			return cq2n(inputText)
		elif mode == "o" :
			return co2n(inputText)
		else :
			sys.exit(0)

	elif args.d :
		mode = spj.SPJ(inputText)
		if mode == "n" :
			return cn2d(inputText)
		elif mode == "d" :
			return kk.myParse(inputText, args.detail)
		elif mode == "q" :
			return cq2d(inputText)
		elif mode == "o" :
			return co2d(inputText)
		else :
			sys.exit(0)

	elif args.q :
		mode = spj.SPJ(inputText)
		if mode == "n" :
			return cn2q(inputText)
		elif mode == "d" :
			return cd2q(inputText)
		elif mode == "q" :
			return kk.myParse(inputText, args.detail)
		elif mode == "o" :
			return co2q(inputText)
		else :
			sys.exit(0)

	elif args.o :
		mode = spj.SPJ(inputText)
		if mode == "n" :
			return cn2o(inputText)
		elif mode == "d" :
			return cd2o(inputText)
		elif mode == "q" :
			return cq2o(inputText)
		elif mode == "o" :
			return kk.myParse(inputText, args.detail)
		else :
			sys.exit(0)

	else :
		sys.exit(0)

# コマンドライン引数の解析
parser = argparse.ArgumentParser(description = "詳しくはこちらをご覧下さい(https://pypi.org/project/csw/)。")

parser.add_argument("-v", "--version", action = "version", version = "%(prog)s 0.3.4")
parser.add_argument("--n2d", action = "store_true", help = "平叙文肯定から平叙文否定への変換")
parser.add_argument("--n2q", action = "store_true", help = "平叙文肯定から疑問文への変換")
parser.add_argument("--n2o", action = "store_true", help = "平叙文肯定か命令文への変換")

parser.add_argument("--d2n", action = "store_true", help = "平叙文否定から平叙文肯定への変換")
parser.add_argument("--d2q", action = "store_true", help = "平叙文否定から疑問文への変換")
parser.add_argument("--d2o", action = "store_true", help = "平叙文否定から命令文への変換")

parser.add_argument("--q2n", action = "store_true", help = "疑問文から平叙文肯定への変換")
parser.add_argument("--q2d", action = "store_true", help = "疑問文から平叙文否定への変換")
parser.add_argument("--q2o", action = "store_true", help = "疑問文から命令文への変換")

parser.add_argument("--o2n", action = "store_true", help = "命令文から平叙文肯定への変換")
parser.add_argument("--o2d", action = "store_true", help = "命令文から平叙文否定への変換")
parser.add_argument("--o2q", action = "store_true", help = "命令文から疑問文への変換")

parser.add_argument("--n", action = "store_true", help = "平叙文肯定への変換")
parser.add_argument("--d", action = "store_true", help = "平叙文否定への変換")
parser.add_argument("--q", action = "store_true", help = "疑問文への変換")
parser.add_argument("--o", action = "store_true", help = "命令文への変換")

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

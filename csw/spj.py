import re
import MeCab
import os

Dfeatures  = ["ない", "無い", "なかっ", "無かっ", "ません"]

def SPJ(inputText):
	tagger = MeCab.Tagger()
	
	# 空文字列をparseすることでnode.surfaceのバグをケアする
	tagger = MeCab.Tagger("-d /var/lib/mecab/dic/ipadic-utf8")
	# 半角記号を全角にする
	inputText = inputText.replace("!", "！")
	inputText = inputText.replace(",", "、")
	inputText = inputText.replace(".", "。")
	inputText = inputText.replace("，", "、")
	inputText = inputText.replace("．", "。")

	# ！と。を前の文に含んで分割
	inputLines = []
	outputLines = []
	inputLines = re.split("(?<=。|！)", inputText)
	
	if '' in inputLines :
		inputLines.remove('')

	lineCount = len(inputLines)

	for i in range(0, lineCount, 1) :
		# inputLines[i]をノードとして扱う
		node = tagger.parseToNode(inputLines[i])

		# 形態素解析したときの行数(\nの数)を取得
		length = tagger.parse(inputLines[i]).count(os.linesep)

		parts = []
		tmpSurface = 0
		tmp1 = 0
		tmp2 = 0
		tmp3 = 0
		tmp4 = 0
		tmp5 = 0
		tmp6 = 0
		meCount = 0
		changeFlag = 0

		while node:
			# 表層語を取ってくる
			tmpSurface = node.surface

			# 品詞を取ってくる
			tmp1 = node.feature.split(",")[0]
			tmp2 = node.feature.split(",")[1]
			tmp3 = node.feature.split(",")[2]
			tmp4 = node.feature.split(",")[3]
			tmp5 = node.feature.split(",")[4]
			tmp6 = node.feature.split(",")[5]
			tmp7 = node.feature.split(",")[6]

			if tmpSurface != "" :
				parts.append([tmpSurface, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7])

			meCount += 1
			if meCount == length:
				break

			# ノードを進める
			node = node.next

		if tmp1 != "記号" :
			parts.append(["!。！", "記号", "**", "**", "**", "**", "**", "**"])

		partsLength = len(parts)

		outputText = "tekitoudayo"

		for j in range(partsLength - 1, -1, -1) :
			if parts[j][0] == "？" or (parts[j][0] == "。" or parts[j][0] == "！") and parts[j - 1][0] == "か":
				sp = "q"
				break

			elif parts[j][0] in Dfeatures :
				sp = "d"
				break

			elif "命令" in parts[j][6] :
				sp = "o"
				break

			else :
				sp = "n"

	return sp

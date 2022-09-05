import re
import MeCab
import os

AverbSpecial = ["ぬ", "まい"]

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

		verbCount = 0

		for j in range(partsLength - 1, -1, -1) :
			if parts[j][1] == "動詞" :
				verbCount += 1
			if parts[j][0] == "？" or (parts[j][0] == "。" or parts[j][0] == "！") and parts[j - 1][0] == "か":
				sp = "q"
				break

			elif (partsLength - 1 >= j + 2 and "非" not in parts[j][2] and parts[j + 1][0] == "ませ" and parts[j + 1][1] == "助動詞" and "命令" not in parts[j + 1][6] and (parts[j + 3][0] == "。" or parts[j + 3][2] == "終助詞" or parts[j + 3][1] == "助動詞")) or (partsLength - 1 >= j + 1 and parts[j + 1][0] in AverbSpecial and parts[j + 1][1] == "助動詞" and parts[j + 2][1] == "記号") or (j - 1 >= 0 and parts[j - 1][2] != "副助詞" and "非" not in parts[j][2] and partsLength - 1 >= j + 1 and (parts[j + 1][0] == "ない" or parts[j + 1][0] == "無い") and (parts[j + 1][1] == "助動詞" and ("非" not in parts[j][2] or "非" in parts[j][2] and parts[j][6] == "未然形" or (partsLength - 1 >= j + 3 and parts[j + 2][1] == "名詞" and "非" in parts[j + 2][2] and parts[j + 3][1] == "助動詞")) or (parts[j][1] == "助詞" or parts[j][1] == "動詞") and (parts[j + 1][1] == "形容詞" or parts[j][2] == "副助詞")) and (parts[j + 2][1] == "助動詞" and "デス" in parts[j + 2][5] or parts[j + 2][1] == "記号" or parts[j + 2][2] == "終助詞" or "ダ" in parts[j + 2][5] and parts[j + 2][6] == "未然形" or parts[j + 2][1] == "名詞" and "非" in parts[j + 2][2] and parts[j + 3][1] == "助動詞")) or (j - 1 >= 0 and parts[j - 1][2] != "副助詞" and "非" not in parts[j][2] and partsLength - 1 >= j + 1 and (parts[j + 1][0] == "ない" or parts[j + 1][0] == "無い") and (parts[j + 1][1] == "助動詞" and ("非" not in parts[j][2] or "非" in parts[j][2] and parts[j][6] == "未然形" or (partsLength - 1 >= j + 3 and parts[j + 2][1] == "名詞" and "非" in parts[j + 2][2] and parts[j + 3][1] == "助動詞")) or (parts[j][1] == "助詞" or parts[j][1] == "動詞") and (parts[j + 1][1] == "形容詞" or parts[j][2] == "副助詞")) and (parts[j + 2][1] == "助動詞" and "デス" in parts[j + 2][5] or parts[j + 2][1] == "記号" or parts[j + 2][2] == "終助詞" or "ダ" in parts[j + 2][5] and parts[j + 2][6] == "未然形" or parts[j + 2][1] == "名詞" and "非" in parts[j + 2][2] and parts[j + 3][1] == "助動詞")) or (j - 1 >= 0 and parts[j - 1][2] != "副助詞" and partsLength - 1 >= j + 1 and (parts[j + 1][0] == "なかっ" or parts[j + 1][0] == "無かっ") and (parts[j + 1][1] == "助動詞" and ("非" not in parts[j][2] or "非" in parts[j][2] and parts[j][6] == "未然形") or (parts[j][1] == "助詞" or parts[j][1] == "動詞") and parts[j + 1][1] == "形容詞") and parts[j + 2][0] == "た" and (parts[j + 3][1] == "記号" or parts[j + 3][1] == "名詞" and "非" in parts[j + 3][2] or parts[j + 3][2] == "終助詞" or "ダ" in parts[j + 3][5] and parts[j + 3][6] == "未然形")):
				sp = "d"
				break

			elif ("命令" in parts[j][6] or parts[j][6] == "基本形" and partsLength - 1 >= j + 1 and parts[j + 1][0] == "な") and verbCount == 1:
				sp = "o"
				break

			else :
				sp = "n"

	return sp


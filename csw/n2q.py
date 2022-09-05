import re
import MeCab
import os

def NQ(inputText, det) :
	tagger = MeCab.Tagger("-d /var/lib/mecab/dic/ipadic-utf8")	
	# 空文字列をparseすることでnode.surfaceのバグをケアする
	tagger.parse('')

	# 半角記号を全角にする
	inputText = inputText.replace("!", "！")
	inputText = inputText.replace(",", "、")
	inputText = inputText.replace(".", "。")
	inputText = inputText.replace("，", "、")
	inputText = inputText.replace("．", "。")

	if det :
		print(tagger.parse(inputText))

	# ！と。を前の文に含んで分割
	inputLines = []
	outputLines = []
	inputLines = re.split("(?<=！|。)", inputText)
	
	# 分割したときに出る空白文字列を除去 
	if '' in inputLines :
		inputLines.remove('')

	lineCount = len(inputLines)

	for i in range(0, lineCount, 1) :
		parts = []
		meCount = 0
		changeFlag = 0
		impressFlag = 0

		# inputLines[i]をノードとして扱う
		node = tagger.parseToNode(inputLines[i])

		# 形態素解析したときの行数(\nの数)を取得
		length = tagger.parse(inputLines[i]).count(os.linesep)

		while node :
			# 表層語を取ってくる
			tmpSurface = node.surface

			# 品詞を取ってくる
			tmp1 = node.feature.split(",")[0]
			if tmp1 == "感動詞" :
				impressFlag = 1
			elif impressFlag == 1 and "助" not in tmp1 :
				impressFlag = 0
			tmp2 = node.feature.split(",")[1]
			tmp3 = node.feature.split(",")[2]
			tmp4 = node.feature.split(",")[3]
			tmp5 = node.feature.split(",")[4]
			tmp6 = node.feature.split(",")[5]
			tmp7 = node.feature.split(",")[6]

			if tmp2 == "終助詞" :
				inputLines[i] = inputLines[i][::-1].replace(tmp2, '', 1)[::-1]
			
			elif tmpSurface != "" :
				parts.append([tmpSurface, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7])

			meCount += 1
			if meCount == length :
				break

			# ノードを進める
			node = node.next

		partsLength = len(parts)

		j1 = partsLength - 4
		j2 = partsLength - 3
		j3 = partsLength - 2

		if "？" in inputLines[i] :
			outputLines.append(inputLines[i])
			continue

		if parts[j2][0] == "ん" and parts[j2][1] == "名詞" :
			parts[j2][0] = "の"

		elif parts[j3][0] == "ん" and parts[j3][1] == "名詞" :
			parts[j3][0] = "の"

		if impressFlag == 1 :
			outputText = inputLines[i]

		elif parts[j2][1] == "動詞" and "命令" in parts[j2][6] :
			pass
		
		elif parts[j3][1] == "動詞" and ("命令" in parts[j3][6] or parts[j3][6] == "連用形") :
			pass

		elif parts[j3][0] == "だ" and ("ダ" in parts[j3][5] or "タ" in parts[j3][5]) and parts[j2][2] != "自立" and parts[j3][1] == "助動詞" and parts[j3][6] == "基本形" : 
			parts[j3][0] = "か？"
		
		elif parts[j2][1] == "動詞" and parts[j3][1] == "助動詞":
			parts[j3][0] += "か？"

		elif parts[j2][1] == "名詞" and parts[j3][1] == "助詞" and parts[j3][3] == "連語" :
			parts[j3][0] += "か？"

		elif parts[j2][1] == "名詞" and parts[j3][1] == "助動詞" :
			parts[j3][0] += "か？"

		elif parts[j2][1] == "助詞" and parts[j3][1] == "名詞" :
			parts[j3][0] += "か？"

		elif parts[j2][1] == "助詞" and parts[j3][1] == "連体詞" :
			parts[j3][0] += "か？"

		elif parts[j2][1] == "助詞" and parts[j3][1] == "動詞" :
			parts[j3][0] += "か？"

		elif parts[j3][1] == "助詞" and parts[j3][2] == "特殊" :
			parts[j3][0] = "か？"

		elif parts[j3][1] == "助詞" and "助詞" not in parts[j3][2] and parts[j3][3] != "連語" :
			parts[j3][0] += "か？"
	
		elif parts[j3][1] == "助動詞" and parts[j3][6] == "基本形" :
			parts[j3][0] += "か？"

		elif parts[j3][1] == "動詞" :
			parts[j3][0] += "か？"

		elif parts[j3][1] == "形容詞" :
			parts[j3][0] += "か？"

		elif parts[j3][1] == "副詞" :
			parts[j3][0] += "か？"
		
		elif parts[j3][1] == "名詞" :
			parts[j3][0] += "か？"

		elif parts[j3][2] == "副助詞" :
			parts[j3][0] += "か？"

		elif parts[j3][2] == "接続助詞" :
			parts[j3][0] = "か？"

		# 変換しないとき、そのままにする
		else :
			outputLines.append(inputLines[i])
			continue

		for p in range(0, partsLength, 1) :
			outputLines.append(parts[p][0])

	# ？の後ろの記号を消す
	retLines = ''.join(outputLines)
	retLines = re.sub("(?<=？)\W", "", retLines)
	
	return ''.join(retLines) + '\n'


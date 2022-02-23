import re
import MeCab
import os

def ON(inputText, det) :
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
	inputLines = re.split("(?<=。|！)", inputText)
	
	# 分割したときに出る空白文字列を除去 
	if '' in inputLines :
		inputLines.remove('')

	lineCount = len(inputLines)

	for i in range(0, lineCount, 1) :
		parts = []
		meCount = 0
		addFlag = 0
		changeFlag = 0
		impressFlag = 0
		hukusiFlag = 0

		# inputLines[i]をノードとして扱う
		node = tagger.parseToNode(inputLines[i])

		# 形態素解析したときの行数(\nの数)を取得
		length = tagger.parse(inputLines[i]).count(os.linesep)

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

		# 文末に記号が無いとき、一時的につけて最後に除去する
		if tmp1 != "記号" :
			parts.append(["!。！", "記号", "**", "**", "**", "**", "**", "**"])
			addFlag = 1

		partsLength = len(parts)

		for j in range(0, partsLength, 1) :
			if "命令" in parts[j][6] :
				parts[j][0] = parts[j][7]

			outputLines.append(parts[j][0])

	return ''.join(outputLines).replace("!。！", '') + '\n'

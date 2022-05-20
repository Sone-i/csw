import re
import MeCab
import os

def godanHenkan(change) :
	if change == "い" :
		return change
	elif change in ["か", "き", "く", "こ"] :
		return "け"
	elif change in ["が", "ぎ", "ぐ", "ご"] :
		return "げ"
	elif change in ["さ", "し", "す", "そ"] :
		return "せ"
	elif change in ["た", "ち", "つ", "と"] :
		return "て"
	elif change in ["な", "に", "ぬ", "の"] :
		return "ね"
	elif change in ["ば", "び", "ぶ", "ぼ"] :
		return "べ"
	elif change in ["ま", "み", "む", "も"] :
		return "め"
	elif change in ["ら", "り", "る", "ろ"] :
		return "れ"
	elif change in ["わ", "い", "う", "お"] :
		return "え"
	else :
		return change

def NO(inputText, det) :
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
		outputText = "tekitoudayo"
		meCount = 0
		changeFlag = 0
		impressFlag = 0
		hukusiFlag = 0
		changeHere = 0
		changeSur = "tekitoudayo"

		# inputLines[i]をノードとして扱う
		node = tagger.parseToNode(inputLines[i])

		# 形態素解析したときの行数(\nの数)を取得
		length = tagger.parse(inputLines[i]).count(os.linesep)

		while node:
			# 表層語を取ってくる
			tmpSurface = node.surface

			# 品詞を取ってくる
			tmp1 = node.feature.split(",")[0]
			if tmp1 == "動詞" :
				changeHere = meCount - 1
			
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

		partsLength = len(parts)

		k = changeHere + 1
		while parts[k][1] != "記号" :
			if parts[k][1] == "助動詞" and "タ" in parts[k][5] :
				changeHere = -1
			elif parts[k][1] != "助動詞" and (parts[k][1] != "助詞" or parts[k][2] != "終助詞") and (parts[k][1] != "名詞" or parts[k][2] != "非自立") :
				changeHere = -1
			k += 1

		for j in range(0, partsLength, 1) :
			if j == changeHere and (parts[j + 1][1] == "記号" or parts[j + 1][1] == "助動詞" or (parts[j + 1][1] == "助詞" and parts[j + 1][2] == "終助詞")) :
				if "五段" in parts[j][5] :
					changeSur = parts[j][0]
					change = godanHenkan(parts[j][0][-1:])
					parts[j][0] = parts[j][0][::-1].replace(parts[j][0][-1:], change, 1)[::-1]
					if changeSur != parts[j][0] :
						changeFlag = 1

				elif "一段" in parts[j][5] :
					parts[j][0] = parts[j][7][::-1].replace(parts[j][7][-1:], "ろ", 1)[::-1]
					changeFlag = 1

				elif "サ変" in parts[j][5] :
					parts[j][0] = "しろ"
					changeFlag = 1

				elif "カ変" in parts[j][5] :
					changeFlag = 1
					if parts[j][0] == "来る" :
						parts[j][0] = "来い"
					elif parts[j][0] == "くる" :
						parts[j][0] = "こい"
					else :
						changeFlag = 0

				k = j + 1
				while parts[k][1] != "記号" and changeFlag == 1 :
					if parts[k][1] == "助動詞" or (parts[k][1] == "助詞" and parts[k][2] == "終助詞") or (parts[k][1] == "名詞" and parts[k][2] == "非自立") :
						parts[k][0] = ''
					else :
						break
					k += 1

			outputLines.append(parts[j][0])

	return ''.join(outputLines).replace("!。！", '') + '\n'

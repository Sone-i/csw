import re
import MeCab
import os

def DN(inputText, det) :
	outputText = "tekitoudayo"
	
	checkNai = ["ない", "助動詞", "*", "*","*", "特殊・ナイ", "基本形", "ない"]
	checkKei = ["形容動詞", "動詞"]

	AverbSpecial = ["ぬ", "まい"]

	godanGyoui = ["カ行イ音便", "ガ行"]
	godanGyoultu = ["カ行促音便", "タ行", "ラ行", "ワ行促音便"]
	godanGyousi = ["サ行"]
	godanGyoun = ["ナ行", "バ行", "マ行"]
	waReigai = ["問", "乞", "請"]
	noHenkan = ["ほかなら", "他なら", "はず", "筈", "なくては", "無くては", "しか", "ざるを", "かも", "何も", "なにも"]
	noHenkanFlag = 0

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

			if tmp1 == "副詞" :
				hukusiFlag = 1

			if tmpSurface != "" :
				parts.append([tmpSurface, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7])

			# 文末が「ない」のとき、なにもしない
			if [tmpSurface, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7] == checkNai :
				changeFlag = 1

			meCount += 1
			if meCount == length:
				break

			# ノードを進める
			node = node.next

		if hukusiFlag == 1 :
			outputLines.append(inputLines[i])
			continue

		# 文末に記号が無いとき、一時的につけて最後に除去する
		if tmp1 != "記号" :
			parts.append(["!。！", "記号", "**", "**", "**", "**", "**", "**"])
			addFlag = 1

		partsLength = len(parts)

		for j in range(0, partsLength, 1) :
			for k in range(0, len(noHenkan), 1) :
				if noHenkan[k] in inputLines[i] :
					outputLines.append(inputLines[i])
					noHenkanFlag = 1

			if noHenkanFlag == 1 :
				noHenkanFlag = 0
				break

			if parts[j][2]  == "格助詞" and parts[j + 1][2] == "係助詞" and (parts[j + 2][0] == "ない" or parts[j + 2][0] == "なかっ" or parts[j + 2][0] == "ません") :
				pass

			if partsLength - 1 >= j + 2 and parts[j + 1][0] == "ませ" and parts[j + 1][1] == "助動詞" and "命令" not in parts[j + 1][6] and (parts[j + 3][0] == "。" or parts[j + 3][2] == "終助詞" or parts[j + 3][1] == "助動詞") :
				if j - 1 > 0 and parts[j - 1][2] == "副助詞" :
					pass

				elif partsLength - 1 >= j + 3 and parts[j + 3][0] == "でし" :
					parts[j + 1][0] = "ました"
				
				else :
					parts[j + 1][0] = parts[j + 1][7]

				if parts[j + 1][0] == "ます" :
					k = j + 2
					while parts[k][1] == "助動詞" :
						parts[k][0] = ""
						k += 1

			elif partsLength - 1 >= j + 1 and parts[j + 1][0] in AverbSpecial and parts[j + 1][1] == "助動詞" :
				parts[j][0] = parts[j][7]
				parts[j + 1][0] = ""

			elif j - 1 >= 0 and "ナイ" in parts[j - 1][2] and parts[j][1] != "助動詞" :
				pass

			elif j - 1 >= 0 and parts[j - 1][2] != "副助詞" and partsLength - 1 >= j + 1 and (parts[j + 1][0] == "ない" or parts[j + 1][0] == "無い") and (parts[j + 1][1] == "助動詞" and ("非" not in parts[j][2] or "非" in parts[j][2] and parts[j][6] == "未然形" or (partsLength - 1 >= j + 3 and parts[j + 2][1] == "名詞" and "非" in parts[j + 2][2] and parts[j + 3][1] == "助動詞")) or (parts[j][1] == "助詞" or parts[j][1] == "動詞") and parts[j + 1][1] == "形容詞") and (parts[j + 2][1] == "記号" or parts[j + 2][2] == "終助詞" or "ダ" in parts[j + 2][5] and parts[j + 2][6] == "未然形" or parts[j + 2][1] == "名詞" and "非" in parts[j + 2][2] and parts[j + 3][1] == "助動詞") :
				if j - 1 > 0 and parts[j - 1][1] == "助動詞" and parts[j][1] == "助詞" and parts[j][2] == "係助詞" :
					outputLines.remove(parts[j - 1][0])
					parts[j][0] = parts[j - 1][7]
					parts[j + 1][0] = ''

				elif j - 1 > 0 and parts[j - 1][1] == "助詞" and parts[j - 1][2] != "接続助詞" and parts[j - 1][2] == "格助詞" and parts[j][2] == "係助詞" :
					parts[j][0] = ""
					parts[j + 1][0] = "ある"

				elif j - 1 > 0 and parts[j - 1][2] == "係助詞" and parts[j][1] == "形容詞" :
					parts[j][0] = parts[j][7]
					parts[j + 1][0] = ''

				# 「〜ならない」、「〜いけない」とかも変換しちゃう
				elif parts[j][6] == "未然形" and parts[j + 1][1] == "助動詞" :
					parts[j][0] = parts[j][7]
					parts[j + 1][0] = ''
				
				elif parts[j][6] != "未然形" and j - 1 > 0 and (parts[j - 1][2] == "係助詞" or parts[j - 1][2] == "副助詞") :
					pass

				elif "非" in parts[j - 1][2] and parts[j][1] == "助詞" :
					parts[j + 1][0] = "ある"

				elif "非" not in parts[j - 1][2] and parts[j][2] == "格助詞" :
					parts[j + 1][0] = "ある"

				elif j - 1 > 0 and parts[j - 1][0] == "ば" and parts[j][1] == "動詞" :
					pass

				elif parts[j][1] == "動詞" and "連用" in parts[j + 1][6] :
					pass

				elif parts[j][2] == "係助詞" and parts[j + 1][1] == "形容詞" :
					pass

				elif parts[j][1] == "動詞" and parts[j + 1][1] == "形容詞" :
					parts[j + 1][0] = "る"

				elif j - 1 > 0 and (j - 2 > 0 and parts[j - 2][2] == "格助詞" and parts[j - 1][2] == "係助詞" or parts[j - 1][2] != "係助詞") and parts[j - 1][1] != "副詞" and parts[j][1] == "動詞" :
					parts[j][0] = parts[j][7]
					parts[j + 1][0] = ''

				elif parts[j][1] == "助動詞" and "連用" in parts[j][6] :
					parts[j][0] = parts[j][7]
					parts[j + 1][0] = ''

				elif parts[j][1] == "形容詞" :
					parts[j][0] = parts[j][7]
					parts[j + 1][0] = ''

				elif parts[j][1] == "助詞" :
					parts[j + 1][0] = "ある"

				elif parts[j][2] == "副助詞" :
					parts[j][0] = ''
					parts[j + 1][0] = ''

				#「ならない」を変換してしまう
				# elif parts[j][1] == "動詞" :
				#	print(inputLines[i])

			elif j - 1 >= 0 and parts[j - 1][2] != "副助詞" and partsLength - 1 >= j + 1 and (parts[j + 1][0] == "なかっ" or parts[j + 1][0] == "無かっ") and (parts[j + 1][1] == "助動詞" and ("非" not in parts[j][2] or "非" in parts[j][2] and parts[j][6] == "未然形") or (parts[j][1] == "助詞" or parts[j][1] == "動詞") and parts[j + 1][1] == "形容詞") and parts[j + 2][0] == "た" and (parts[j + 3][1] == "記号" or parts[j + 3][2] == "終助詞" or "ダ" in parts[j + 3][5] and parts[j + 3][6] == "未然形") :
				if parts[j][0] in noHenkan :
					pass

				elif j - 1 > 0 and parts[j - 1][1] == "助動詞" and parts[j][1] == "助詞" and parts[j][2] == "係助詞" :
					outputLines.remove(parts[j - 1][0])
					parts[j][0] = parts[j - 1][7] + "っ"
					parts[j + 1][0] = ''

				elif j - 1 > 0 and parts[j - 1][1] == "助詞" and parts[j - 1][2] != "係助詞" and parts[j][1] == "形容詞" :
					parts[j][0] = parts[j][7][:-1]
					parts[j + 1][0] = "かっ"

				elif j - 1 > 0 and parts[j - 1][2] == "格助詞" and parts[j][2] == "係助詞" and parts[j + 1][1] == "形容詞" :
					parts[j][0] = ""
					parts[j + 1][0] = "あっ"

				elif parts[j][1] == "助詞" and parts[j][2] == "係助詞" and parts[j + 1][1] == "形容詞" :
					parts[j + 1][0] = "あっ"

				elif parts[j][1] == "形容詞" :
					parts[j][0] = parts[j][0][:-1]
					parts[j + 1][0] = parts[j + 1][0][1:]

				elif j - 1 > 0 and parts[j - 1][0] == "ば" and parts[j][1] == "動詞" :
					pass

				elif parts[j][2] == "係助詞" and parts[j + 1][1] == "形容詞" :
					parts[j + 1][0] = "あっ"

				elif parts[j][1] == "動詞" and parts[j + 1][1] == "形容詞" :
					parts[j + 1][0] = ''

				elif parts[j][1] == "助動詞" :
					if "タイ" in parts[j][5] :
						parts[j][0] = parts[j][0][:-1]
						parts[j + 1][0] = parts[j + 1][0][1:]

					elif "イ" in parts[j][5] :
						parts[j][0] = parts[j][0][:-1]
						parts[j + 1][0] = parts[j + 1][0][1:]
					
					else :
						parts[j][0] = parts[j][7]
						parts[j + 1][0] = "っ"

				elif parts[j][1] == "動詞" :
					if "・" not in parts[j][5] :
						parts[j + 1][0] = ''

					elif re.search("(?<=・).+", parts[j][5]).group() in godanGyoultu and parts[j][0][:-1] in waReigai :
						parts[j][0] = parts[j][0][:-1]
						parts[j + 1][0] = "う"

					elif re.search("(?<=・).+", parts[j][5]).group() in godanGyoui :
						parts[j][0] = parts[j][0][:-1]
						parts[j + 1][0] = "い"
	
					elif re.search("(?<=・).+", parts[j][5]).group() in godanGyoultu :
						parts[j][0] = parts[j][0][:-1]
						parts[j + 1][0] = "っ"

					elif re.search("(?<=・).+", parts[j][5]).group() in godanGyousi :
						parts[j][0] = parts[j][0][:-1]
						parts[j + 1][0] = "し"

					elif re.search("(?<=・).+", parts[j][5]).group() in godanGyoun :
						parts[j][0] = parts[j][0][:-1]
						parts[j + 1][0] = "ん"
						parts[j + 2][0] = "だ"

					elif parts[j][2] == "接尾" :
						parts[j][0] = parts[j][0][:-1]
						parts[j + 1][0] = parts[j + 1][0][2:]

					elif "促音" in parts[j][5] :
						parts[j][0] = parts[j][0][:-1]
						parts[j + 1][0] = "っ"

					else :
						parts[j + 1][0] = ''

				elif parts[j][1] == "助詞" :
					parts[j + 1][0] = "あっ"

			else :
				pass

			outputLines.append(parts[j][0])

	return ''.join(outputLines).replace("!。！", '') + '\n'

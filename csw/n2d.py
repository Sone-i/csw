import re
import MeCab
import os

checkNai = ["ない", "助動詞", "*", "*","*", "特殊・ナイ", "基本形", "ない"]
AverbKei = ["たい", "らしい", "たかっ", "らしかっ"]
AverbSpecial = ["ます", "です", "だ", "た", "まし", "でし", "だっ"]
AverbSpecialHen = ["マス", "デス", "ダ", "タ"]
		

def ND(inputText, det):
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
	inputLines = re.split("(?<=。|！|、)", inputText)
	
	if '' in inputLines :
		inputLines.remove('')

	lineCount = len(inputLines)
	mikkeFlag = 0

	for i in range(0, lineCount, 1) :
		# inputLines[i]をノードとして扱う
		node = tagger.parseToNode(inputLines[i])

		# 形態素解析したときの行数(\nの数)を取得
		length = tagger.parse(inputLines[i]).count(os.linesep)

		parts = []
		outputText = "tekitoudayo"
		impressFlag = 0
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

			if tmpSurface != "" :
				parts.append([tmpSurface, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7])

			# 文末が「ない」のとき、なにもしない
			if [tmpSurface, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7] == checkNai :
				changeFlag = 1
			if changeFlag == 1 and tmp1 != "助動詞" and tmp1 != "記号" :
				changeFlag = 0

			meCount += 1
			if meCount == length:
				break

			# ノードを進める
			node = node.next

		if tmp1 != "記号" :
			parts.append(["!。！", "記号", "**", "**", "**", "**", "**", "**"])

		partsLength = len(parts)

		for j in range(0, partsLength, 1) :
			if parts[partsLength - 1][0] == "、" :
				outputLines.append(inputLines[i])
				break

			elif j - 1 >= 0 and parts[j - 1][1] == "感動詞" :
				outputText = parts[j][0]

				changeFlag = 1
				k = j
				while partsLength - 1 >= k :
					if parts[k][1] == "動詞" or parts[k][1] == "形容詞" or parts[k][1] == "形容動詞" :
						changeFlag = 0
					k += 1

			elif (parts[j][0] == "ない" or parts[j][0] == "無い") and (parts[j][1] == "形容詞" or parts[j][1] == "助動詞") and partsLength - 1 >= j + 1 and (parts[j + 1][1] == "助動詞" or parts[j + 1][1] == "記号") and changeFlag == 0 :
				outputText = parts[j][0]

				changeFlag = 1

			elif (parts[j][0] == "なかっ" or parts[j][0] == "無かっ") and parts[j + 1][0] == "た" and changeFlag == 0 :
				outputText = parts[j][0]

				changeFlag = 1

			elif partsLength - 1 >= j + 1 and "接続" in parts[j + 1][2] and (parts[j][0] == "。" or parts[j][0] == "！") :
				outputText = parts[j][0]

			elif parts[j][0] in AverbKei and changeFlag == 0 :
				if parts[j][0] == "たい" :
					outputText = "たくない"

				elif parts[j][0] == "らしい" :
					outputText = "らしくない"

				elif parts[j][0] == "たかっ" :
					outputText = "たくなかっ"

				elif parts[j][0] == "らしかっ" :
					outputText = "らしくなかっ"

				changeFlag = 1

			elif parts[j][0] in AverbSpecial and parts[j - 1][1] != "形容詞" and parts[j - 1][0] == outputText and parts[j + 1][1] != "形容詞" and parts[j + 1][1] != "動詞" and "形容動詞" not in parts[j + 1][2] and not (parts[j - 1][1] == "動詞" and parts[j + 1][1] == "名詞" and "助動詞" not in parts[j + 1][3]) and "副" not in parts[j + 1][2] and parts[j + 1][0] != "、" and changeFlag == 0 :
				if j - 2 >= 0 and parts[j - 2][0] == "ない":
					outputText = parts[j][0]

				elif parts[j][0] == "ます" :
					outputText = "ません"

				elif parts[j][0] == "です" :
					outputText = "じゃないです"

				elif parts[j][0] == "た" :
					outputText = "なかった"

				elif parts[j][0] == "だ" :
				 	outputText = "でない"

				elif parts[j][0] == "まし" :
					outputText = "ませんでし"

				elif parts[j][0] == "でし" :
					outputText = "じゃなかっ"

				elif parts[j][0] == "だっ" :
				 	outputText = "でなかっ"

				changeFlag = 1

			elif "・" in parts[j][5] and re.search("(?<=・).+", parts[j][5]).group() in AverbSpecialHen and parts[j][6] != "連用形" and parts[j][6] != "仮定形" and parts[j - 1][1] != "形容詞" and parts[j - 1][1] != "副詞" and parts[j - 1][0] == outputText and parts[j + 1][1] != "形容詞" and parts[j + 1][1] != "動詞" and "形容動詞" not in parts[j + 1][2] and not (parts[j - 1][1] == "動詞" and parts[j + 1][1] == "名詞") and ("副" not in parts[j + 1][2] or (parts[j - 1][1] == "名詞" and "非" not  in parts[j - 1][2])) and changeFlag == 0 :
				if "マス" in parts[j][5] :
					outputText = "ません"

				elif "デス" in parts[j][5] :
					outputText = "じゃないです"

				elif "タ" in parts[j][5] :
					outputText = "なかった"

				elif "ダ" in parts[j][5] :
					outputText = "でない"

				changeFlag = 1

				k = j + 1
				while partsLength - 1 >= k :
					if parts[k][1] == "名詞" or parts[k][1] == "動詞" or parts[k][1] == "形容詞" :
						break
					k += 1

				if partsLength == k :
					k = j + 1
					while partsLength - 1 >= k and (parts[k][1] == "助動詞" or parts[k][1] == "副詞") :
						parts[k] = ["", "", "", "", "", "", "", ""]
						k += 1

			elif parts[j][1] == "連体詞" and (partsLength - 1 == j or partsLength - 1 >= j + 1 and parts[j + 1][1] == "記号") and changeFlag == 0 :
				if parts[j + 1][0] == "。" or parts[j + 1][0] == "！" :
					outputText = parts[j][0] + "でない"

				else :
					outputText = parts[j][0]

			elif parts[j][1] == "形容詞" and partsLength - 1 >= j + 1 and parts[j + 1][1] == "名詞" :
				outputText = parts[j][0]

			elif parts[j][1] == "形容詞" and changeFlag == 0 :
				changeFlag = 1
				
				if "未然" in parts[j][6] :
					outputText = parts[j][7][:-1] + parts[j][0].replace(parts[j][7][:-1], "くな", 1) 
			
				elif "連用" in parts[j][6] and "並立" not in parts[j + 1][2]:
					if "タ" in parts[j][6] :
						outputText = parts[j][7][:-1] + parts[j][0].replace(parts[j][7][:-1], "くな", 1) 

					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif parts[j][6] == "基本形" :
					if parts[j][0] == "いい" :
						outputText = "よくない"

					else :
						outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "いなく", 1)[::-1]
				
				elif parts[j][6] == "仮定形" :
					outputText = parts[j][7][:-1] + parts[j][0].replace(parts[j][7][:-1], "くな", 1) 

				else :
					outputText = parts[j][0]
					changeFlag = 0

			elif "形容動詞" in parts[j - 1][2] and parts[j][6] == "基本形" and changeFlag == 0 :
				outputText = parts[j][0] + "でない"

				changeFlag = 1

			elif "助動詞" in parts[j - 1][3] and "非" not in parts[j - 1][2] and changeFlag == 0 :
				changeFlag = 1

				if "形容詞" in parts[j][5] :
					outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "いなで", 1)[::-1]

				elif "副詞" in parts[j][2] :
					outputText = parts[j][0]
					changeFlag = 0

				else :
					outputText = "でない"

			elif partsLength - 1 >= j + 1 and parts[j + 1][0] == "まい" and changeFlag == 0 :
				outputText = parts[j][0]

			elif parts[j][0] == "ある" and parts[j][1] == "動詞" and changeFlag == 0 :
				outputText = "ない"
				
				changeFlag = 1

			elif parts[j][0] == "あっ" and parts[j][1] == "動詞" and ("ワ" in parts[j][5] or "ラ" in parts[j][5]) and changeFlag == 0 :
				outputText = "なかっ"
				
				changeFlag = 1

			elif parts[j][0] == "ある" and parts[j][1] == "助動詞" and changeFlag == 0 :
				outputText = "ない"
				
				changeFlag = 1

			elif parts[j][1] == "副詞" and (partsLength - 1 == j or partsLength - 1 >= j + 1 and parts[j + 1][1] == "記号") and changeFlag == 0 :
				if parts[j + 1][0] == "。" or parts[j + 1][0] == "！" :
					outputText = parts[j][0] + "でない"

				else :
					outputText = parts[j][0]

			elif j - 1 >= 0 and parts[j][1] == "副詞" and "助詞" not in parts[j][2] and partsLength - 1 >= j + 1 and "連体" not in parts[j + 1][2] and parts[j + 1][1] != "助動詞" and parts[j + 1][1] != "形容詞" and parts[j + 1][1] != "副詞" and parts[j + 1][1] != "名詞" and parts[j + 1][1] != "感動詞" and changeFlag == 0 :
				outputText = parts[j][0] + "でない"
				
				changeFlag = 1

				k = j + 1
				while partsLength - 1 >= k :
					if parts[k][1] == "名詞" or parts[k][1] == "動詞" or parts[k][1] == "形容詞" :
						break
					k += 1

				if partsLength == k :
					k = j + 1
					while partsLength - 1 >= k and (parts[k][1] == "助動詞" or parts[k][1] == "副詞") :
						parts[k] = ["", "", "", "", "", "", "", ""]
						k += 1

				if partsLength - 1 >= j + 1 and parts[j + 1][2] == "連体化" :
					parts[j + 1] = ["", "", "", "", "", "", "", ""]

			elif parts[j][1] == "名詞" and (partsLength - 1 == j or partsLength - 1 >= j + 1 and parts[j + 1][1] == "記号" and "非" not in parts[j][2]) and changeFlag == 0 :
				if parts[j][2] != "接尾" and parts[j][3] != "人名" and (parts[j + 1][0] == "。" or parts[j + 1][0] == "！") :
					outputText = parts[j][0] + "でない"
				else :
					outputText = parts[j][0]

			elif parts[j][1] == "名詞" and "助動詞" in parts[j + 1][1] and partsLength - 1 >= j + 2 and parts[j + 2][1] == "名詞" and changeFlag == 0 :
				outputText = parts[j][0]

			elif parts[j][1] == "名詞" and "助動詞" in parts[j + 1][1] and changeFlag == 0 :
				if parts[j + 1][0] in AverbSpecial :
					outputText = parts[j][0]
					
					changeFlag = 0

				else :
					outputText = parts[j][0]

			elif parts[j][1] == "動詞" and partsLength - 1 >= j + 1 and parts[j + 1][1] == "名詞" and "非" not in parts[j + 1][2]:
				outputText = parts[j][0]

			elif "命令" in parts[j][6] and changeFlag == 0 :
				if  j - 1 >= 0 and "係" in parts[j - 1][2] :
					outputText = parts[j][0]

				else :
					outputText = parts[j][0][::-1].replace(parts[j][0][::-1], "な" + parts[j][7][::-1], 1)[::-1]
					changeFlag = 1

			elif partsLength - 1 >= j + 2 and parts[j][1] == "動詞" and "連用" in parts[j][6] and parts[j + 1][1] == "助動詞" and (parts[j + 2][1] == "名詞" and "助動詞" not in parts[j + 2][3]) and  changeFlag == 0 :
				outputText = parts[j][0]

			elif "五段" in parts[j][5] and changeFlag == 0 :
				changeFlag = 1

				if "未然" in parts[j][6] :
					if parts[j + 1][0] == "う" :
						kata = re.search("(?<=・).", parts[j][5])
						change = "".join(chr(ord(kata.group()) - 96))
						outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "よいでいな" + change, 1)[::-1]

					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif "連用" in parts[j][6] and "非" not in parts[j][2] :
					if "命令" in parts[j + 1][6] :
						outputText = parts[j][0]
					
					elif partsLength - 1 >= j + 2 and "副" in parts[j + 2][2] and parts[j + 2][1] != "助詞" :
						outputText = parts[j][0]
						changeFlag = 0

					elif "助動詞" in parts[j + 1][3] :
						kata = re.search("(?<=・).", parts[j][5])
						change = "".join(chr(ord(kata.group()) - 96))
						outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "な" + change, 1)[::-1]

					elif parts[j + 1][1] == "助動詞" :
						if parts[j + 1][0] == "た" or parts[j + 1][0] == "だ" :
							kata = re.search("(?<=・).", parts[j][5])
							change = "".join(chr(ord(kata.group()) - 96))
							outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "っかな" + change, 1)[::-1]

							kata = re.search("(?<=・).", parts[j + 1][5])
							change = "".join(chr(ord(kata.group()) - 96))
							parts[j + 1][0] = parts[j + 1][0].replace(parts[j + 1][0][0], change)

						else :
							outputText = parts[j][0]
							changeFlag = 0

					elif "接続" in parts[j + 1][2] and partsLength - 1 >= j + 2 and (parts[j + 2][0] == "。"or parts[j + 2][0] == "！") :
						outputText = parts[j][0][::-1].replace(parts[j][0][::-1], "な" + parts[j][7][::-1], 1)[::-1]
						parts[j + 1] = ["", "", "", "", "", "", "", ""]
						changeFlag = 1

					elif "終助詞" in parts[j + 1][2] :
						outputText = parts[j][0][::-1].replace(parts[j][0][::-1], "な" + parts[j][7][::-1], 1)[::-1]

					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif "連用" in parts[j][6] and "非" in parts[j][2] and parts[j - 1][1] != "動詞" :
					if parts[j + 1][1] == "助動詞" :
						if parts[j + 1][0] not in AverbKei and parts[j + 1][0][0] == "た" or parts[j + 1][0][0] == "だ" :
							kata = re.search("(?<=・).", parts[j][5])
							change = "".join(chr(ord(kata.group()) - 96))
							outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "っかな" + change, 1)[::-1]
							
							kata = re.search("(?<=・).", parts[j + 1][5])
							change = "".join(chr(ord(kata.group()) - 96))
							parts[j + 1][0] = parts[j + 1][0].replace(parts[j + 1][0], change)
						
						else :
							outputText = parts[j][0]
							changeFlag = 0

					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif parts[j][6] == "基本形" or parts[j][6] == "連体形" :
					if partsLength - 1 >= j + 1 and ("接続" in parts[j + 1][2] or "接続" in parts[j + 1][6]) :
						outputText = parts[j][0]
						changeFlag = 0

					elif partsLength - 1 >= j + 1 and "副" in parts[j + 1][2] or "格" in parts[j + 1][2] :
						outputText = parts[j][0]
						changeFlag = 0

					elif "非" not in parts[j][2] and partsLength - 1 >= j + 1 and "非" in parts[j + 1][2] :
						outputText = parts[j][0]
						changeFlag = 0

					else :
						kata = re.search("(?<=・).", parts[j][5])
						change = "".join(chr(ord(kata.group()) - 96))
						outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "いな" + change, 1)[::-1]
			
				elif parts[j][6] == "仮定形" :
					kata = re.search("(?<=・).", parts[j][5])
					change = "".join(chr(ord(kata.group()) - 96))
					outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "れけな" + change, 1)[::-1]

				else :
					outputText = parts[j][0]
					changeFlag = 0
			
			elif "一段" in parts[j][5] and changeFlag == 0 :
				changeFlag = 1

				if "未然" in parts[j][6] :
					if parts[j][0][-1:] == "よ" and parts[j + 1][0] == "う" :
						outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "よいでいな", 1)[::-1]

					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif "連用" in parts[j][6] and "非" not in parts[j][2] :
					if "命令" in parts[j + 1][6] :
						outputText = parts[j][0]
					
					elif partsLength - 1 >= j + 2 and "副" in parts[j + 2][2] :
						outputText = parts[j][0]
						changeFlag = 0

					elif parts[j + 1][1] == "助動詞" :
						if parts[j + 1][0] == "た" or parts[j + 1][0] == "だ" :
							outputText = parts[j][0] + "なかっ"

						elif parts[j + 1][0] == "ます" :
							outputText = parts[j][0]
							changeFlag = 0
						
						elif parts[j + 1][6] == "仮定形" :
							outputText = parts[j][0] + "なかっ"
						
						else :
							outputText = parts[j][0]
							changeFlag = 0

					elif "接続" in parts[j + 1][2] and partsLength - 1 >= j + 2 and (parts[j + 2][0] == "。"or parts[j + 2][0] == "！") :
						outputText = parts[j][0][::-1].replace(parts[j][0][::-1], "な" + parts[j][7][::-1], 1)[::-1]
						parts[j + 1] = ["", "", "", "", "", "", "", ""]
						changeFlag = 1

					elif "終助詞" in parts[j + 1][2] :
						outputText = parts[j][0][::-1].replace(parts[j][0][::-1], "な" + parts[j][7][::-1], 1)[::-1]

					else :
						outputText = parts[j][0]
						changeFlag = 0
				
				elif "連用" in parts[j][6] and "非" in parts[j][2] and parts[j - 1][1] != "動詞" :
					if parts[j + 1][1] == "助動詞" :
						if parts[j + 1][0] == "た" or parts[j + 1][0] == "だ" :
							outputText = parts[j][0] + "なかっ"

						elif parts[j + 1][0] == "ます" :
							outputText = parts[j][0]
							changeFlag = 0
						
						else :
							outputText = parts[j][0]
							changeFlag = 0

					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif parts[j][6] == "基本形" or parts[j][6] == "連体形" :
					if partsLength - 1 >= j + 1 and parts[j + 1][1] == "名詞" and "非" in parts[j + 1][2]:
						outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "いな", 1)[::-1]

					elif partsLength - 1 >= j + 1 and ("接続" in parts[j + 1][2] or "接続" in parts[j + 1][6]) :
						outputText = parts[j][0]
						changeFlag = 0

					elif partsLength - 1 >= j + 1 and "副" in parts[j + 1][2] or "格" in parts[j + 1][2] :
						outputText = parts[j][0]
						changeFlag = 0

					elif "非" not in parts[j][2] and partsLength - 1 >= j + 1 and "非" in parts[j + 1][2] :
						outputText = parts[j][0]
						changeFlag = 0

					else :
						outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "いな", 1)[::-1]
				
				elif parts[j][6] == "仮定形" :
					#outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "れけな", 1)[::-1]
					
					outputText = parts[j][0]
					changeFlag = 0

				else :
					outputText = parts[j][0]
					changeFlag = 0
			
			elif "カ変" in parts[j][5] and changeFlag == 0 :
				changeFlag = 1
				koFlag = 0

				if "未然" in parts[j][6] :
					if parts[j][0][-1:] == "よ" and parts[j + 1][0] == "う" :
						outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "よいでいな", 1)[::-1]
						koFlag = 1

					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif "連用" in parts[j][6] :
					if "命令" in parts[j + 1][6] :
						outputText = parts[j][0]
					
					elif partsLength - 1 >= j + 2 and "副" in parts[j + 2][2] :
						outputText = parts[j][0]
						changeFlag = 0

					elif parts[j + 1][1] == "助動詞" :
						if parts[j + 1][0] == "た" or parts[j + 1][0] == "だ" :
							outputText = parts[j][0] + "なかっ"
							koFlag = 1

						elif parts[j + 1][0] == "ます" :
							outputText = parts[j][0]
							changeFlag = 0

						else :
							outputText = parts[j][0]
							changeFlag = 0

					elif "接続" in parts[j + 1][2] and partsLength - 1 >= j + 2 and (parts[j + 2][0] == "。"or parts[j + 2][0] == "！") :
						outputText = parts[j][0][::-1].replace(parts[j][0][::-1], "な" + parts[j][7][::-1], 1)[::-1]
						parts[j + 1] = ["", "", "", "", "", "", "", ""]
						changeFlag = 1

					elif "終助詞" in parts[j + 1][2] :
						outputText = parts[j][0][::-1].replace(parts[j][0][::-1], "な" + parts[j][7][::-1], 1)[::-1]
						koFlag = 1

					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif parts[j][6] == "基本形" or parts[j][6] == "連体形" :
					if partsLength - 1 >= j + 1 and ("接続" in parts[j + 1][2] or "接続" in parts[j + 1][6]) :
						outputText = parts[j][0]
						changeFlag = 0

					elif partsLength - 1 >= j + 1 and "副" in parts[j + 1][2] or "格" in parts[j + 1][2] :
						outputText = parts[j][0]
						changeFlag = 0

					elif "非" not in parts[j][2] and partsLength - 1 >= j + 1 and "非" in parts[j + 1][2] :
						outputText = parts[j][0]
						changeFlag = 0

					else :
						outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "いな", 1)[::-1]
						koFlag = 1

				elif parts[j][6] == "仮定形" :
					outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "れけな", 1)[::-1]
					koFlag = 1

				else :
					outputText = parts[j][0]
					changeFlag = 0

				if "来" not in parts[j][0] and koFlag == 1 :
					outputText = outputText.replace(parts[j][0][0], "こ")
					koFlag = 0

			elif "サ変" in parts[j][5] and "スル" in parts[j][5] and parts[j][1] == "動詞" and changeFlag == 0 :
				changeFlag = 1

				if "未然" in parts[j][6] :
					if parts[j][0][-1:] == "よ" and parts[j + 1][0] == "う" :
						outputText = parts[j][0][::-1].replace(parts[j][0][-1:], "よいでいな", 1)[::-1]

					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif "連用" in parts[j][6] and "非" not in parts[j][2] :
					if "命令" in parts[j + 1][6] :
						outputText = parts[j][0]
					
					elif partsLength - 1 >= j + 2 and "副" in parts[j + 2][2] :
						outputText = parts[j][0]
						changeFlag = 0

					elif parts[j + 1][1] == "助動詞" :
						if parts[j + 1][0] == "た" :
							if partsLength - 1 >= j + 2 and (parts[j + 2][1] == "動詞" or "副" in parts[j + 2][2]) :
								outputText = parts[j][0]
								changeFlag = 0
							
							else :
								outputText = parts[j][0] + "なかっ"

						else :
							outputText = parts[j][0]
							changeFlag = 0

					elif "接続" in parts[j + 1][2] and partsLength - 1 >= j + 2 and (parts[j + 2][0] == "。"or parts[j + 2][0] == "！") :
						outputText = parts[j][0][::-1].replace(parts[j][0][::-1], "な" + parts[j][7][::-1], 1)[::-1]
						parts[j + 1] = ["", "", "", "", "", "", "", ""]
						changeFlag = 1

					elif "終助詞" in parts[j + 1][2] :
						outputText = parts[j][0][::-1].replace(parts[j][0][::-1], "な" + parts[j][7][::-1], 1)[::-1]

					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif "連用" in parts[j][6] and "非" in parts[j][2] and parts[j - 1][1] != "動詞" :
					if parts[j + 1][1] == "助動詞" :
						if parts[j + 1][0] == "た" :
							if partsLength - 1 >= j + 2 and (parts[j + 2][1] == "動詞" or "副" in parts[j + 2][2]) :
								outputText = parts[j][0]
								changeFlag = 0
							
							else :
								outputText = parts[j][0] + "なかっ"

						else :
							outputText = parts[j][0]
							changeFlag = 0
				
					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif parts[j][6] == "基本形" or parts[j][6] == "連体形" :
					if partsLength - 1 >= j + 1 and ("接続" in parts[j + 1][2] or "接続" in parts[j + 1][6]) :
						outputText = parts[j][0]
						changeFlag = 0

					elif partsLength - 1 >= j + 1 and "副" in parts[j + 1][2] or "格" in parts[j + 1][2] :
						outputText = parts[j][0]
						changeFlag = 0
	
					elif "非" not in parts[j][2] and partsLength - 1 >= j + 1 and "非" in parts[j + 1][2] :
						outputText = parts[j][0]
						changeFlag = 0

					else :
						outputText = parts[j][0][::-1].replace("るす", "いなし", 1)[::-1]
				
				elif parts[j][6] == "仮定形" :
					outputText = parts[j][0][::-1].replace("れす", "れけなし", 1)[::-1]

				else :
					outputText = parts[j][0]
					changeFlag = 0
			
			elif "サ変" in parts[j][5] and "ズル" in parts[j][5] and "未然" not in parts[j][6] and parts[j][1] == "動詞" and changeFlag == 0 :
				changeFlag = 1

				if "連用" in parts[j][6] and "非" not in parts[j][2] :
					if "命令" in parts[j + 1][6] :
						outputText = parts[j][0]
					
					elif partsLength - 1 >= j + 2 and "副" in parts[j + 2][2] :
						outputText = parts[j][0]
						changeFlag = 0

					elif parts[j + 1][1] == "助動詞" :
						if parts[j + 1][0] == "た" :
							outputText = parts[j][0] + "なかっ"
						
						elif parts[j + 1][0] == "ます" :
							outputText = parts[j][0]
							changeFlag = 0
				
						else :
							outputText = parts[j][0]
							changeFlag = 0

					elif "接続" in parts[j + 1][2] and partsLength - 1 >= j + 2 and (parts[j + 2][0] == "。"or parts[j + 2][0] == "！") :
						outputText = parts[j][0][::-1].replace(parts[j][0][::-1], "な" + parts[j][7][::-1], 1)[::-1]
						parts[j + 1] = ["", "", "", "", "", "", "", ""]
						changeFlag = 1

					elif "終助詞" in parts[j + 1][2] :
						outputText = parts[j][0][::-1].replace(parts[j][0][::-1], "な" + parts[j][7][::-1], 1)[::-1]

					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif "連用" in parts[j][6] and "非" in parts[j][2] and parts[j - 1][1] != "動詞" :
					if parts[j + 1][1] == "助動詞" :
						if parts[j + 1][0] == "た" :
							outputText = parts[j][0] + "なかっ"
						
						elif parts[j + 1][0] == "ます" :
							outputText = parts[j][0]
							changeFlag = 0
				
						else :
							outputText = parts[j][0]
							changeFlag = 0
				
					else :
						outputText = parts[j][0]
						changeFlag = 0

				elif parts[j][6] == "基本形" or parts[j][6] == "連体形" :
					if partsLength - 1 >= j + 1 and ("接続" in parts[j + 1][2] or "接続" in parts[j + 1][6]) :
						outputText = parts[j][0]
						changeFlag = 0

					elif partsLength - 1 >= j + 1 and "副" in parts[j + 1][2] or "格" in parts[j + 1][2] :
						outputText = parts[j][0]
						changeFlag = 0

					elif "非" not in parts[j][2] and partsLength - 1 >= j + 1 and "非" in parts[j + 1][2] :
						outputText = parts[j][0]
						changeFlag = 0

					else :
						outputText = parts[j][0][::-1].replace("るず", "いなじ", 1)[::-1]
				
				elif parts[j][6] == "仮定形" :
					outputText = parts[j][0][::-1].replace("れず", "れけなじ", 1)[::-1]

				else :
					outputText = parts[j][0]
					changeFlag = 0
			
			else :
				outputText = parts[j][0]

			k = j + 1
			checkKei = ["形容動詞", "動詞"]
			while k <= partsLength - 1 and parts[k][0] != "、" :
				if (parts[k][1] in checkKei or parts[k][5] in checkKei) and "未然" not in parts[k][6] :
					outputText = parts[j][0]
					changeFlag = 0
				k += 1
				
			outputLines.append(outputText)

	return ''.join(outputLines).replace("!。！", '') + '\n'


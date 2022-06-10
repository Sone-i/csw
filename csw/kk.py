# -*- coding: utf-8

import MeCab
import os

def myParse(inputText, det) :
	tagger = MeCab.Tagger("-d /var/lib/mecab/dic/ipadic-utf8")
	if det :
		print(tagger.parse(inputText))

	return inputText.strip() + "\n"

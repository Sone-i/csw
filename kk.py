# -*- coding: utf-8

import MeCab
import os

def myParse(inputText) :
	tagger = MeCab.Tagger("-d /var/lib/mecab/dic/ipadic-utf8")
	print(tagger.parse(inputText))

	return inputText

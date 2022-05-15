# 文自在変換ツール(Convert Sentences at Will)
これは平叙文肯定や平叙文否定、疑問文、命令文など、様々な文型からなる日本語の文章を互いに変換することができるツールです。<br />
文章の形態素解析を行い、変換をルールベースによって実現しています。<br />
コマンド終了後、ImportError: cannot import name 'main' from 'csw.csw'&nbsp;のようなエラーが出力されますが、動作には問題ありません。<br />
Google Colaboratoryでの実行も可能です。<br />

# 環境
Linux OS もしくは Google Colaboratory<br />
Python 3系<br />
MeCab<br />
ipadic-utf8(/var/lib/mecab/dic/&nbsp;にインストールされていること)<br />

# 使い方
n：平叙文肯定,&nbsp;d：平叙文否定,&nbsp;q：疑問文,&nbsp;o：命令文<br />
-c,&nbsp;--current：一文ずつ入出力<br />
-d,&nbsp;--detail：形態素解析結果を表示<br />
-f,&nbsp;--file：ファイルによる入出力(その後ろに変換元ファイル名、変換先ファイル名を順に指定)<br />

# 使用例
**csw --n2d --current --detail もしくは csw --n2d -cd**
- 平叙文肯定から平叙文否定への変換を一文ずつの入出力で行います。

**csw --q --file hoge.txt piyo.txt もしくは csw --q -f hoge.txt piyo.txt**
- 様々な文型の文章で構成されたhoge.txtを全て疑問文に変換し、それらをpiyo.txtへ上書きします。

# 実行例
```
$ csw --n2d -cd
「e」か「え」を入力で終了

---------------------------------------------
input  : 私は人間です。
私	名詞,代名詞,一般,*,*,*,私,ワタシ,ワタシ
は	助詞,係助詞,*,*,*,*,は,ハ,ワ
人間	名詞,一般,*,*,*,*,人間,ニンゲン,ニンゲン
です	助動詞,*,*,*,特殊・デス,基本形,です,デス,デス
。	記号,句点,*,*,*,*,。,。,。
EOS

output : 私は人間じゃないです。
---------------------------------------------
input  : e
```

<br />

```
$ csw --d -f input.txt output.txt
$
```

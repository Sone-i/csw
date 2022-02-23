# 文自在変換ツール(Convert Sentences at Will)
これは平叙文肯定や平叙文否定、疑問文、命令文など、様々な文型からなる日本語の文章を互いに変換することができるツールです。<br />
文章の形態素解析を行い、変換をルールベースによって実現しています。<br />
**pip install git+https://github.com/Sone-i/csw** とコマンドを打つことでインストール可能です。<br />
コマンド終了後、 ImportError: cannot import name 'main' from 'csw.csw' のようなエラーが出力されますが、動作には問題ありません。<br />

# 環境
Linux OS<br />
Python 3系<br />
MeCab<br />
ipadic-utf8(/var/lib/mecab/dic/ にインストールされていること)<br />

# 使い方
n：平叙文肯定, d：平叙文否定, q：疑問文, o：命令文<br />
-cur：一文ずつ入出力, -det：形態素解析結果を表示, -file：ファイルによる入出力<br />

# 使用例
**csw -n2d -cur -det**
- 平叙文肯定から平叙文否定への変換を一文ずつ入出力で行います。

**csw -q2n -file**
- 疑問文から平叙文肯定への変換をファイルによる入出力で行います。コマンド実行後、ファイルを指定できます。

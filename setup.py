# -*- coding: utf-8

import setuptools
import csw

with open('README.md', 'r') as fh:
	long_description = fh.read()

setuptools.setup(
	name = 'csw',
	version = csw.__version__,
	author = 'Sone-i',
	author_email = 'i18308@kagawa.kosen-ac.jp',
	description = "文自在変換ツール",
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/Sone-i/csw',
	download_url = 'https://github.com/Sone-i/csw',
	packages = setuptools.find_packages(),
	classifiers = [
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
	],
	entry_points = {
		'console_scripts': ['csw = csw.csw:main']
	},
	python_requires = '>=3.7',
	install_requires = [
		'MeCab>=0.996'
	]
)

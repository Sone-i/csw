import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="csw",
	version="0.1.0",
	author="Sone-i",
	author_email="i18308@kagawa.kosen-ac.jp",
	description="This is csw test.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/Sone-i/csw",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
	],
	entry_points = {
		'console_scripts': ['csw = csw.csw:main']
	},
	python_requires='>=3.7',
)

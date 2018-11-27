all:
	mona run pub -P
	mona checkout -p /pub
	latexmk -cd -pdf pub/paper.tex

distclean:
	rm -rf venv __pycache__ .mona calcs pub

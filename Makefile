all: run

venv:
	python3 -m venv venv

install:
	pip install mona[sci,cli,graphviz] matplotlib

init:
	mona init

run:
	mona run mona_demo:pub -P
	mona checkout -p /pub
	latexmk -cd -pdf pub/paper.tex

distclean:
	rm -rf venv .mona calcs pub

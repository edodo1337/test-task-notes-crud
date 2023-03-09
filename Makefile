UNAME=$(shell uname -s)

style:
	flake8 .

types:
	mypy .

test:
	pytest -q --cov=. --cov-report=xml

check:
	make test style types

install-hooks:
	pre-commit install -t pre-commit -t commit-msg -t pre-push

.PHONY: all format format-check pylint mypy test
current_dir=$(CURDIR)
all: mypy

# sort imports and auto-format python code
format:
	isort -rc src/ tests/ --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=88 -o onmt -o torch
	black -t py37 src/ tests/

format-check:
	(isort -rc src/ tests/ --check-only --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=88 -o onmt -o torch) && (black -t py37 --check src/ tests/) || (echo "run \"make format\" to format the code"; exit 1)

pylint: format-check 
	pylint -j0 src/ tests/

mypy: pylint
	mypy --show-error-codes src/ tests/

test: mypy $(shell find tests/ -name "*.py" -type f)
	python -m pytest -n auto --durations=0 tests/

docker-dev-image:
	docker build -t dataflow-graph-program-image -f Dockerfile .

run-dev-image:
	docker run --name dataflow_graph_program_dev_container -t -d --mount src=$(current_dir),target=/dataflow,type=bind dataflow-graph-program-image /bin/bash

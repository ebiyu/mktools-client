.PHONY: test
test:
	python -m pipenv run test

.PHONY: build
build:
	python -m pipenv run build

%:
	python -m pipenv run $@

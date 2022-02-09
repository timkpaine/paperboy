version = `python setup.py --version 2>/dev/null`

run:  ## run server
	python -m paperboy.server

runnoauth:  ## run server without auth
	python -m paperboy.server --auth='none'

runlocal:  ## run server with sql backend, local scheduler
	python -m paperboy.server --backend='sqla' --auth='sqla' --scheduler='local'

runsql_airflow:  ## run server with sql backend, airflow scheduler
	python -m paperboy.server --backend='sqla' --auth='sqla' --scheduler='airflow'

runsql_luigi:  ## run server with sql backend, luigi scheduler
	python -m paperboy.server --backend='sqla' --auth='sqla' --scheduler='luigi'

rundummy:  ## run server with sql backend
	python -m paperboy.server --backend='sqla' --auth='sqla' --scheduler='dummy'

tests: clean ## Clean and Make unit tests
	python -m pytest -v tests --cov=paperboy --junitxml=python_junit.xml --cov-report=xml --cov-branch

testjs: clean ## run the js tests for travis CI
	yarn
	yarn test

test: clean lint ## run the tests for travis CI
	@ python -m pytest -v tests --cov=paperboy
	yarn
	yarn test

lint: ## run linter
	python -m flake8 paperboy setup.py
	yarn lint

fix:  ## run black
	python -m black paperboy/  setup.py
	./node_modules/.bin/tslint --fix src/ts/**/*.ts

annotate: ## MyPy type annotation check
	python -m mypy -s paperboy

annotate_l: ## MyPy type annotation check - count only
	python -m mypy -s paperboy | wc -l

clean: ## clean the repository
	find . -name "__pycache__" | xargs  rm -rf
	find . -name "*.pyc" | xargs rm -rf
	rm -rf .coverage cover htmlcov logs build dist *.egg-info
	make -C ./docs clean || echo

js:  ## build the js
	yarn
	yarn build

build:  ## build the repository
	python setup.py build

install:  ## install to site-packages
	python setup.py install

docs:  ## make documentation
	make -C ./docs html && open docs/_build/html/index.html

dist:  js  ## dist to pypi
	rm -rf dist build
	python setup.py sdist
	python setup.py bdist_wheel
	python -m twine check dist/* && twine upload dist/*
	git commit -a -m "Release $(version)"; true
	git tag v$(version)
	git push --tags

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: clean run test tests help annotate annotate_l docs run build js dist

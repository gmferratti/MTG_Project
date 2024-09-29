test:
	cd tests && python -m unittest discover -s tests
create-env:
run:


clean:
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache

lint-all: # verifica e formata os arquivos
	black . && \
	flake8 && \
	isort .

lint: # apenas verifica
	flake8 .
	black --check .
	isort --check .

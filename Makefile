test:
	cd tests && python -m unittest discover -s tests
create-env:
run:


clean:
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache

lint-all: # verifica e formata os arquivos
	cd mtg-project && \
	black . && \
	flake8 && \
	isort .

lint: # apenas verifica
	cd mtg-project && \
	flake8 . && \
	black --check . && \
	isort --check .

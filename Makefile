test:
	python -m unittest tests.classes.test_deck

clean:
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache
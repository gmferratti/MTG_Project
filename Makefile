test:
	cd tests && python -m unittest discover -s tests


clean:
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache
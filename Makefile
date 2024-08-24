test:
	python -m unittest test_deck.py

clean:
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache
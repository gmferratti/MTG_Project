create-env:
	conda create -n mtg_curve_env python=3.12
	echo "source $(shell conda info --base)/etc/profile.d/conda.sh && conda activate mtg_curve_env && pip install -r requirements.txt" > temp_script.sh
	bash temp_script.sh
	rm temp_script.sh
	
run:


clean:
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache
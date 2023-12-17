.PHONY: install opt experiment tests app

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	# $$ pip list --format=freeze > requirements.txt #run this to create requirements.txt

opt:
	python optimization/optimize_parameters.py

experiment:
	python experiments/run_experiment.py

tests:
	pytest tests/

app:
	streamlit run app/app.py

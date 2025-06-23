.PHONY: data preprocess notebooks clean

data:
	python -m energy_analysis.data_ingest

preprocess:
	python -m energy_analysis.preprocessing

notebooks:
	for nb in Notebooks/*.ipynb; do \
	  jupyter nbconvert --to notebook --execute $$nb \
	    --ExecutePreprocessor.timeout=600 \
	    --output executed/"$$(basename $$nb)" ; \
	done

clean:
	rm -rf data/processed/*
	rm -rf executed/*

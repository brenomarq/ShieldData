install:
	pip install -r requirements.txt
	python -m spacy download pt_core_news_sm

test:
	pytest tests/

process:
	python src/preprocessing.py --input "data/raw/Hackathon Participa DF Data.xlsx" --output "data/processed/Hackathon Participa DF Data Processado.xlsx"

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__

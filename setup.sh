pip install -r requirements.txt

# Install spacy and sci spacy
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_md
python -m spacy download es_core_news_md
python -m spacy download pt_core_news_md


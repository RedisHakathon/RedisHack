import opendatasets as od
import json
import pandas as pd
import re
import string
from sentence_transformers import SentenceTransformer
import pickle



#download the arxiv dataset from kaggle 
#useneme & kaggle token
#od.download("https://www.kaggle.com/datasets/Cornell-University/arxiv")


DATA_PATH = "arxiv-metadata-oai-snapshot.json"
YEAR_CUTOFF = 2012
YEAR_PATTERN = r"(19|20[0-9]{2})"
ML_CATEGORY = "cs.LG"

def process(paper: dict):
    paper = json.loads(paper)
    if paper['journal-ref']:
        years = [int(year) for year in re.findall(YEAR_PATTERN, paper['journal-ref'])]
        years = [year for year in years if (year <= 2022 and year >= 1991)]
        year = min(years) if years else None
    else:
        year = None
    return {
        'id': paper['id'],
        'title': paper['title'],
        'year': year,
        'authors': paper['authors'],
        'categories': ','.join(paper['categories'].split(' ')),
        'abstract': paper['abstract']
    }

def papers():
    with open(DATA_PATH, 'r') as f:
        for paper in f:
            paper = process(paper)
            if paper['year']:
                if paper['year'] >= YEAR_CUTOFF and ML_CATEGORY in paper['categories']:
                    yield paper

#load papers into dataframe
df = pd.DataFrame(papers())


#function for further cleaning
def clean_description(description: str):
    if not description:
        return ""
    # remove unicode characters
    description = description.encode('ascii', 'ignore').decode()

    # remove punctuation
    description = re.sub('[%s]' % re.escape(string.punctuation), ' ', description)

    # clean up the spacing
    description = re.sub('\s{2,}', " ", description)

    # remove urls
    #description = re.sub("https*\S+", " ", description)

    # remove newlines
    description = description.replace("\n", " ")

    # remove all numbers
    #description = re.sub('\w*\d+\w*', '', description)

    # split on capitalized words
    description = " ".join(re.split('(?=[A-Z])', description))

    # clean up the spacing again
    description = re.sub('\s{2,}', " ", description)

    # make all words lowercase
    description = description.lower()

    return description

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
emb = model.encode(df.apply(lambda r: clean_description(r['title'] + ' ' + r['abstract']), axis=1).tolist())

with open('arxiv_embeddings_10000.pkl', 'wb') as f:
    data = pickle.dumps(df)
    f.write(data)
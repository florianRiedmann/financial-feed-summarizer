import os
import datetime
import numpy as np
import pandas as pd
from scraper import create_DataFrame


def make_directory():
    project_dir = os.path.dirname(__file__)
    path = os.path.join(project_dir, 'feeds', str(datetime.date.today()))
    try:
        os.mkdir(path)
    except FileExistsError:
        print('Directory already exists.')
    finally:
        print('Directory created.')
    return path

def export_to_csv():
    path = make_directory()
    df = create_DataFrame()
    print(df)
    df.to_csv(os.path.join(path, str(datetime.date.today()) + '_financial_feeds.csv'))
    return None

def export_clean_sentence_to_csv()
    # export cleaned sentences do DataFrame
    pd.DataFrame(sentences).to_csv(os.path.join(project_dir, "clean_text/sentences.csv"), header=False, index=False)
    pd.DataFrame(clean_sentences).to_csv(os.path.join(project_dir, "clean_text/clean_sentences.csv"), header=False, index=False)
    return None

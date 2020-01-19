import os
import datetime
import numpy as np
import pandas as pd
from scraper import create_DataFrame


def make_directory():
    project_dir = os.path.dirname(__file__)
    path = os.path.join(project_dir, 'data', str(datetime.date.today()))
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

def export_clean_sentence_to_csv(series1, series2):
    path = make_directory()
    timestamp = datetime.date.today()
    # export clean and clean clean sentences do DataFrame
    pd.DataFrame(series1).to_csv(os.path.join(path, f"{timestamp}_clean_sentences.csv"), header=False, index=False)
    pd.DataFrame(series2).to_csv(os.path.join(path, f"{timestamp}_clean_clean_sentences.csv"), header=False, index=False)
    return None

def export_summary(data):
    path = make_directory()
    timestamp = datetime.date.today()
    data.nlargest(20, 'Score').to_csv(os.path.join(path, f"{timestamp}_summary_top20.csv"), header=False, index=False)
    data.to_csv(os.path.join(path, f"{timestamp}_summary.csv"), header=False, index=False)
    return None

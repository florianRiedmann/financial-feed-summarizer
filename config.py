import os


CHECK_DEPENDENCIES = True
CHECK_DIRECTORIES = True

SCRAPE_DATA = False
GENERATE_NEW_VECTORS = False
CLUSTER_ARTICLES = True
SUMMARIZE_ARTICLES = True

GLOBAL_RANDOM_SEED = 42

PROJECT_DIR = os.path.dirname(__file__)
GLOVE_PATH = os.path.join(PROJECT_DIR, "glove")
GLOVE_FILE_NAME = "glove.6B.100d.txt"
RESULTS_PATH = os.path.join(PROJECT_DIR, "step_results")
PICKLES_PATH = os.path.join(PROJECT_DIR, "pickles")
PLOTS_PATH = os.path.join(PROJECT_DIR, "plots")
JSON_FILE_NAME = "feeds.json"
SCRAPED_DATA_FILE_NAME = "step_results/scraped_data.csv"
CLEAN_ARTICLE_FILE_NAME = "step_results/clean_article.csv"
CLEAN_SENTENCE_FILE_NAME = "step_results/clean_sentences.csv"
CLUSTERED_ARTICLE_FILE_NAME = "step_results/clustered_articles.csv"
SUMMARIZED_ARTICLE_FILE_NAME = "step_results/summarized_articles.csv"
VECTOR_PICKLE_FILE_NAME = "pickles/article_vector.pickle"
SILHOUETTE_SCORE_PLOT_FILE_NAME = "plots/silhouette_scores.png"

SUMMARY_SENTENCE_NUMBER = 3

import os

# Initializing
CHECK_DEPENDENCIES = True
CHECK_DIRECTORIES = True

# Pipeline
SCRAPE_DATA = True
GENERATE_NEW_VECTORS = True
CLUSTER_ARTICLES = True
SUMMARIZE_ARTICLES = False

# Random Seed
GLOBAL_RANDOM_SEED = 42

# Directories
PROJECT_DIR = os.path.dirname(__file__)
GLOVE_PATH = os.path.join(PROJECT_DIR, "glove")
GLOVE_FILE_NAME = "glove.6B.100d.txt"
RESULTS_PATH = os.path.join(PROJECT_DIR, "step_results")
PICKLES_PATH = os.path.join(PROJECT_DIR, "pickles")
PLOTS_PATH = os.path.join(PROJECT_DIR, "plots")
JSON_FILE_NAME = "feeds.json"
SCRAPED_DATA_FILE_NAME = os.path.join(PROJECT_DIR, "step_results/scraped_data.csv")
CLEAN_ARTICLE_FILE_NAME = os.path.join(PROJECT_DIR, "step_results/clean_article.csv")
CLEAN_SENTENCE_FILE_NAME = os.path.join(PROJECT_DIR, "step_results/clean_sentences.csv")
CLUSTERED_ARTICLE_FILE_NAME = os.path.join(PROJECT_DIR, "step_results/clustered_articles.csv")
SUMMARIZED_ARTICLE_FILE_NAME = os.path.join(PROJECT_DIR, "step_results/summarized_articles.csv")
VECTOR_PICKLE_FILE_NAME = os.path.join(PROJECT_DIR, "pickles/article_vector.pickle")
SILHOUETTE_SCORE_PLOT_FILE_NAME = os.path.join(PROJECT_DIR, "plots/silhouette_scores.png")

# Number of Sentences in Summary
SUMMARY_SENTENCE_NUMBER = 3

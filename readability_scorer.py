import readability


# Install scorer with:
# pip install https://github.com/andreasvc/readability/tarball/master

def get_readability_score(text):
    results = readability.getmeasures(text, lang='en')
    return results['readability grades']['FleschReadingEase']

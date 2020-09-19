from rake_nltk import Metric, Rake

r = Rake(min_length=1, max_length=3, ranking_metric=Metric.WORD_DEGREE)

def get_keywords(product_reviews):
    results = []
    for i in range(len(product_reviews)):
        product_review = product_reviews.iloc[i]
        r.extract_keywords_from_text(product_review["review_headline"] + ". " + product_review["review_body"])
        results.append(r.get_ranked_phrases())
    print('keywords:', results)
    return results

def get_aggregate_keywords(product_reviews):
    strings = []
    for i in range(len(product_reviews)):
        product_review = product_reviews.iloc[i]
        strings.append(product_review["review_headline"])
        strings.append(product_review["review_body"])
    r.extract_keywords_from_sentences(strings)
    result = r.get_ranked_phrases()
    print('aggregate keywords:', result)
    return result

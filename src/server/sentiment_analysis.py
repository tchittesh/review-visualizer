from collections import defaultdict

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sentiment_analyzer = SentimentIntensityAnalyzer()

pos_neg_cutoff = 0.5
neutral_cutoff = 0.7

def get_review_sentiments(product_reviews):
    counts = defaultdict(int)
    for i in range(len(product_reviews)):
        product_review = product_reviews.iloc[i]
        star_rating = product_review["star_rating"]
        review_headline = product_review["review_headline"]
        review_body = product_review["review_body"]

        polarity_scores = sentiment_analyzer.polarity_scores(review_headline + review_body)
        if polarity_scores["pos"] > pos_neg_cutoff:
            counts["very positive"] += 1
        elif polarity_scores["neg"] > pos_neg_cutoff:
            counts["very negative"] += 1
        elif polarity_scores["neu"] > neutral_cutoff:
            counts["neutral"] += 1
        elif polarity_scores["pos"] > polarity_scores["neg"]:
            counts["positive"] += 1
        else:
            counts["negative"] += 1

    return counts

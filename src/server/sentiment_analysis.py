from collections import defaultdict

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sentiment_analyzer = SentimentIntensityAnalyzer()

def get_review_sentiments(product_reviews):
    counts = defaultdict(int)
    for i in range(len(product_reviews)):
        product_review = product_reviews.iloc[i]
        star_rating = product_review["star_rating"]
        review_headline = product_review["review_headline"]
        review_body = product_review["review_body"]

        polarity_scores = sentiment_analyzer.polarity_scores(review_headline + review_body)
        if polarity_scores["pos"] > 0.5:
            counts["very positive"] += 1
        elif polarity_scores["neg"] > 0.5:
            counts["very negative"] += 1
        elif polarity_scores["neu"] > 0.5:
            counts["neutral"] += 1
        elif polarity_scores["pos"] > polarity_scores["neg"]:
            counts["positive"] += 1
        else:
            counts["negative"] += 1

    return counts

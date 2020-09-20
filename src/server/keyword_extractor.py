from collections import defaultdict
import math

from fuzzywuzzy import fuzz
from rake_nltk import Metric, Rake


r = Rake(min_length=1, max_length=3, ranking_metric=Metric.WORD_DEGREE)


def get_keywords(product_reviews):
    results = []
    for i in range(len(product_reviews)):
        product_review = product_reviews.iloc[i]
        r.extract_keywords_from_text(product_review["review_headline"] + ". " + product_review["review_body"])
        results.append(r.get_ranked_phrases())
    return results


def get_aggregate_keywords(product_reviews, max_keywords = 20, improve_quality = True):
    strings = []
    for i in range(len(product_reviews)):
        product_review = product_reviews.iloc[i]
        strings.append(product_review["review_headline"])
        strings.append(product_review["review_body"])
    r.extract_keywords_from_sentences(strings)
    if improve_quality:
        top_2n_keywords = r.get_ranked_phrases()[:2*max_keywords]
        # get pairwise fuzzy distances
        G = {}
        for i in range(len(top_2n_keywords)):
            for j in range(len(top_2n_keywords)):
                if i == j:
                    continue
                kw1 = top_2n_keywords[i]
                kw2 = top_2n_keywords[j]
                p1, p2 = (kw2, kw1) if len(kw1) < len(kw2) else (kw2, kw1)
                G[(i, j)] = fuzz.ratio(p1, p2)
        scores = [sum(G[(i, j)] for j in range(len(top_2n_keywords)) if i != j) for i in range(len(top_2n_keywords))]
        # choose lowest n similarity scores
        top_n_indices = sorted(list(range(len(top_2n_keywords))), key = lambda i: scores[i])[:max_keywords]
        return [top_2n_keywords[i] for i in top_n_indices]
    else:
        return r.get_ranked_phrases()[:max_keywords]


def get_pros_and_cons(product_reviews, count = 3):
    negative_reviews = product_reviews.loc[product_reviews["star_rating"].isin(["1", "2"])]
    positive_reviews = product_reviews.loc[product_reviews["star_rating"].isin(["4", "5"])]

    if len(negative_reviews) == 0:
        cons = ["_"] * count
    else:
        cons = get_aggregate_keywords(negative_reviews, max_keywords = 3)

    if len(positive_reviews) == 0:
        pros = ["_"] * count
    else:
        pros = get_aggregate_keywords(positive_reviews, max_keywords = 3)

    return {
        "cons": cons,
        "pros": pros,
    }


class KeywordReviewGraph():

    def __init__(self, product_reviews, max_keywords = 20):
        product_reviews_neg = product_reviews.loc[product_reviews["star_rating"].isin(["1", "2"])]
        self.neg_review_count = len(product_reviews_neg)
        product_reviews_pos = product_reviews.loc[product_reviews["star_rating"].isin(["3", "4", "5"])]
        self.keywords = []
        for product_reviews_type in [product_reviews_neg, product_reviews_pos]:
            if len(product_reviews_type) == 0:
                continue
            num_keywords = int(math.ceil(len(product_reviews_type) / len(product_reviews) * max_keywords)) + 1
            self.keywords.extend(get_aggregate_keywords(product_reviews_type, max_keywords = num_keywords))
        self.keywords = self.keywords[:max_keywords]
        self.product_reviews = product_reviews

        self.graph = defaultdict(list) # maps keywords to (review number, match score) and review number to (keyword, match score)
        self.keyword_review_pair_to_match_score = {}
        for keyword in self.keywords:
            for i in range(len(product_reviews)):
                product_review = self.product_reviews.iloc[i]
                review_summary = product_review["review_headline"] + " " + product_review["review_body"]
                match_score = fuzz.ratio(keyword, review_summary)
                self.graph[keyword].append([i, match_score])
                self.graph[i].append([keyword, match_score])
                self.keyword_review_pair_to_match_score[(keyword, i)] = match_score

        count, total = 0, 0
        for keyword in self.keywords:
            for i in range(len(self.product_reviews)):
                count += 1
                total += self.keyword_review_pair_to_match_score[(keyword, i)]
        avg_match_score = total / count
        self.min_match_score = 4/3 * avg_match_score

    def compute_keyword_frequencies(self):
        keyword_frequencies = {}
        for keyword in self.keywords:
            frequency = 0
            for _, match_score in self.graph[keyword]:
                if match_score > self.min_match_score:
                    frequency += 1
            keyword_frequencies[keyword] = frequency
        return keyword_frequencies

    def compute_keyword_valences(self):
        star_to_valence = {"1": -1, "2": -0.5, "3": 0, "4": 0.5, "5": 1}
        keyword_to_valence = {}

        for keyword in self.keywords:
            total_weight = 0
            total_valence = 0
            for i, weight in self.graph[keyword]:
                product_review = self.product_reviews.iloc[i]
                if weight < self.min_match_score:
                    weight = weight / 20
                else:
                    weight = weight * 20
                if int(product_review["star_rating"]) < 3:
                    weight *= len(self.product_reviews) / self.neg_review_count
                total_weight += weight
                total_valence += star_to_valence[product_review["star_rating"]] * weight
            if total_weight == 0:
                keyword_to_valence[keyword] = 0
            else:
                keyword_to_valence[keyword] = total_valence / total_weight

        return keyword_to_valence

    def compute_keyword_pair_probabilities(self):
        keyword_pair_to_probability = {
            keyword: {}
            for keyword in self.keywords
        } # maps (kw1, kw2) to Pr(kw2 appears | kw1 appears)

        for keyword1 in self.keywords:
            for keyword2 in self.keywords:
                if keyword1 == keyword2:
                    continue

                keyword1_count = 0
                keyword1and2_count = 0
                for i in range(len(self.product_reviews)):
                    if self.keyword_review_pair_to_match_score[(keyword1, i)] < self.min_match_score:
                        continue
                    keyword1_count += 1
                    if self.keyword_review_pair_to_match_score[(keyword2, i)] >= self.min_match_score:
                        keyword1and2_count += 1

                if keyword1_count == 0:
                    keyword_pair_to_probability[keyword1][keyword2] = 0
                else:
                    keyword_pair_to_probability[keyword1][keyword2] = keyword1and2_count / keyword1_count

        return keyword_pair_to_probability


    def get_word_graph(self):

        return {
            "keywords": self.keywords,
            "keyword_valences": self.compute_keyword_valences(),
            "keyword_pair_probabilities": self.compute_keyword_pair_probabilities(),
            "keyword_frequencies": self.compute_keyword_frequencies(),
        }

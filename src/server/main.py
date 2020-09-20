from flask import Flask, request, abort
from flask_cors import CORS

from load import load_amazon_dataset
from sentiment_analysis import get_review_sentiments
from time_series_data import get_moving_star_avg
from keyword_extractor import KeywordReviewGraph, get_pros_and_cons

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

dataset = load_amazon_dataset('../../data/amazon_reviews_us_Wireless_v1_00.tsv', max_reviews = None)
product_names = set([name.lower() for name in dataset["product_title"]])

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/suggestions')
def suggest():
    input_name = request.args.get('product_name')
    if input_name is None:
        abort(400)

    suggestions = []
    for product_name in product_names:
        if input_name == product_name[:len(input_name)]:
            suggestions.append(product_name)
        if len(suggestions) == 5:
            break

    for product_name in product_names:
        if input_name in product_name and input_name not in suggestions:
            suggestions.append(product_name)
        if len(suggestions) == 5:
            break

    return {
        "suggestions": suggestions
    }


@app.route('/visualize')
def get_visualization_data():
    input_name = request.args.get('product_name')
    if input_name is None:
        abort(400)

    product_id, product_name = None, None
    for i in range(len(dataset)):
        if input_name in dataset["product_title"][i]:
            product_id = dataset["product_id"][i]
            product_name = dataset["product_title"][i]
            break
    if product_id is None:
        abort(400)

    product_reviews = dataset.loc[dataset["product_id"] == product_id]

    overall_sentiment_results = get_review_sentiments(product_reviews)
    graph = KeywordReviewGraph(product_reviews)
    word_graph = graph.get_word_graph()
    pros_and_cons = get_pros_and_cons(product_reviews)
    time_series = get_moving_star_avg(product_reviews)


    return {
        "overall_sentiment": overall_sentiment_results,
        "word_graph": word_graph,
        "pros_and_cons": pros_and_cons,
        "product_name": product_name,
        "time_series": time_series,
    }

if __name__ == '__main__':
    app.run()

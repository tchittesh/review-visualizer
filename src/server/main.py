from flask import Flask, request

from load import load_amazon_dataset
from sentiment_analysis import get_review_sentiments

app = Flask(__name__)

dataset = load_amazon_dataset('./amazon_reviews_us_Wireless_v1_00.tsv')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/visualize')
def get_visualization_data():
    input_name = request.args.get('product_name')

    product_id = None
    for i in range(len(dataset)):
        if input_name in x["product_title"][i]:
            product_id = x["product_id"][i]
            break
    if product_id is None:
        return {}

    product_reviews = dataset.loc[dataset["product_id"] == product_id]
    overall_sentiment_results = get_overall_sentiment(product_reviews)


    return {
        "overall_sentiment": overall_sentiment_results
    }

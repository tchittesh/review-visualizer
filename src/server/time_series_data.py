from load import load_amazon_dataset

dataset = load_amazon_dataset('../../data/amazon_reviews_us_Wireless_v1_00.tsv', max_reviews = None)
input_name = "LG G4 Case Hard Transparent Slim Clear Cover for LG G4"


product_id = None
for i in range(len(dataset)):
    if input_name in dataset["product_title"][i]:
        product_id = dataset["product_id"][i]
        break

product_reviews = dataset.loc[dataset["product_id"] == product_id]


# return a time series, where value at each time is an average of star ratings up to that point,
# but older reviews are weighted less than recent ones
def get_moving_star_avg(product_reviews):
    # assumes reviews sorted by date
    group_by_date = []
    last_date = ""
    scores = []
    for i in range(len(product_reviews)):
        product_review = product_reviews.iloc[i]
        star_rating = product_review["star_rating"]
        review_date = product_review["review_date"]
        if review_date == last_date:
            scores.append(int(star_rating))
        elif last_date == "":
            last_date = review_date
            scores.append(int(star_rating))
        else:
            avg_rating = sum(scores) / len(scores)
            group_by_date.append((last_date, avg_rating, len(scores)))
            scores = [int(star_rating)]
            last_date = review_date
    avg_rating = sum(scores) / len(scores)
    group_by_date.append((last_date, avg_rating))

    res = []

    # do some sort of weighting here

    return group_by_date




print(get_decaying_star_avg_over_time(product_reviews))

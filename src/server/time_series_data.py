
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
    group_by_date.append((last_date, avg_rating, len(scores)))

    res = []
    cumulative_sum = 0
    cumulative_ct = 0
    for i in range(len(group_by_date)):
        # do some sort of weighting here
        (d, suml, ct) = group_by_date[i]
        cumulative_ct += ct
        cumulative_sum += suml
        res.append({'date': d, 'value': cumulative_sum / cumulative_ct})

    return res

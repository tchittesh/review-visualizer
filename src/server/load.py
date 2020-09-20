import pandas as pd
import csv
from utils import remove_line_breaks

def load_amazon_dataset(path, max_reviews = 100000):
    '''Returns pd.DataFrame containing the dataset'''

    data = []
    column_names = None
    review_body_index = None
    with open(path) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for i, row in enumerate(rd):
            if i == 0:
                column_names = row
                review_body_index = column_names.index("review_body")
            elif len(row) == 15:
                row[review_body_index] = remove_line_breaks(row[review_body_index])
                data.append(row)
            if max_reviews is not None and len(data) >= max_reviews:
                break
    return pd.DataFrame(data, columns = column_names)

import pandas as pd
import csv
from utils import remove_line_breaks
from os.path import exists

def load_amazon_dataset(path, max_reviews = 100000):
    '''Returns pd.DataFrame containing the dataset'''
    pickle_path = path + '.pkl'
    if exists(pickle_path):
        print('Loading from pickle at', pickle_path)
        return pd.read_pickle(pickle_path)
    print('Constructing pickle at', pickle_path)
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
    result = pd.DataFrame(data, columns=column_names)
    result.to_pickle(pickle_path)
    return result

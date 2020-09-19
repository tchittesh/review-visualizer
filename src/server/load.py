import pandas as pd
import csv

def load_amazon_dataset(path, max_reviews = 100000):
    '''Returns pd.DataFrame containing the dataset'''

    data = []
    column_names = None
    with open(path) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for i, row in enumerate(rd):
            if i == 0:
                column_names = row
            elif len(row) == 15:
                data.append(row)
            if len(data) > max_reviews:
                break
    return pd.DataFrame(data, columns = column_names)

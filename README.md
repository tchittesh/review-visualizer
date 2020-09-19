# review-visualizer

Made for HackMIT 2020. A tool that presents visualizations of aggregate Amazon product
review data to provide quick at-a-glance insights with more relevant detail than simple star averages.

### Features
* Uses sentiment analysis to give more detail on review comment contents
* Extracts keywords to summarize most frequently mentioned pros/cons across reviews
* Generates a time series for a moving average of star reviews over time, to account
for stale information and changing needs of users over time

## Setup

Download amazon dataset into root directory.

### Server setup

export FLASK_APP=src/server/main.py
flask run // or python -m flask run


### Frontend setup

```
cd src/frontend/rv-frontend
npm start
```

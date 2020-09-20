import React, { useState, useEffect } from 'react';
import './App.css';
import Search from './components/search-bar.js'
import DoubleChart from './components/two-sided-chart.js';
import TimeSeries from './components/time_series.js';
import WordGraph from './components/word-graph.js';
import { FiHeart } from 'react-icons/fi'
const request = require('request');

function App() {
  const [inputValue, setInputValue] = useState("");
  const [showResult, setShowResult] = useState(false);
  const [sentiment_display, set_sentiment_display] = useState({})
  const [time_series_data, set_time_series_data] = useState([])
  const [prod_name, set_prod_name] = useState("")
  const [word_graph, set_word_graph] = useState({})

  function searchOnChange(event) {
    event.preventDefault();
    setInputValue(event.target.value);
  }

  function submitForm(event) {
    event.preventDefault();

    console.log('request submitted')

    // make request to the backend endpoint
    request.get({
      url: 'http://127.0.0.1:5000/visualize?product_name=' + inputValue
    }, function (err, httpResponse, body) {
      if (err) {
        alert(err);
        return
      }
      body = JSON.parse(body)
      console.log(body);
      set_prod_name(inputValue);
      set_time_series_data(body['time_series']);
      set_sentiment_display(body['overall_sentiment'])
      set_word_graph(body['word_graph']);

    })

  }

  function isEmpty(obj) {
    for (var key in obj) {
      if (obj.hasOwnProperty(key)) {
        return false;
      }
    }
    return true;
  }

  useEffect(() => {
    if (!isEmpty(sentiment_display) && !isEmpty(word_graph)) {
      setShowResult(true);
    }
  }, [sentiment_display, word_graph])

  function formatDoubleChart(body, prod_name) {
    if (!body) {
      return
    }
    return (
      <DoubleChart vnegative={body["very negative"] || 0}
                   negative={body["negative"] || 0}
                   positive={body["positive"] || 0}
                   vpositive={body["very positive"] || 0}
                   name={prod_name}
      />
    )
  }

  // TODO: loading animation
  // TODO: change two sided chart colors
  // TODO: hover for information

  return (
    <div className="App">
      {!showResult &&
      <header className="App-header">
        <div className="title">Review Visualizer</div>
        <div className="subtitle">Presenting concise product review insights through data visualization.</div>
        <br/>
        <Search inputValue={inputValue}
                onChange={searchOnChange}
                onSubmit={submitForm}/>

      </header>
      }
      {showResult &&
        <div>
          <Search inputValue={inputValue}
                  onChange={searchOnChange}
                  onSubmit={submitForm}/>
          <div className="summary-text">Now showing review data summary for <strong>{prod_name}</strong></div>
          <div className="chart-summary">
            {formatDoubleChart(sentiment_display, prod_name)}
            <TimeSeries input={time_series_data}/>
          </div>
          <WordGraph graph={word_graph}/>
        </div>
      }

      <footer>
        Made with <FiHeart/> for HackMIT 2020. <a href="https://github.com/tchittesh/review-visualizer">View on Github</a>
      </footer>

    </div>
  );
}

export default App;

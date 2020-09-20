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
  const [isLoading, setIsLoading] = useState(false);
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

    setIsLoading(true);
    // make request to the backend endpoint
    request.get({
      url: 'http://127.0.0.1:5000/visualize?product_name=' + inputValue
    }, function (err, httpResponse, body) {
      if (err) {
        alert(err);
        setIsLoading(false);
        setShowResult(false);
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
      setIsLoading(false);
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

  let dots = document.getElementsByClassName('loading-dot');
  function startLoad(){
    Array.prototype.forEach.call(dots, function(el,index){
      dots[index].style.display = "none";
      setTimeout(function(){
        dots[index].style.display = "inline-block";
      },1000 + (1000 * index))
    })
  }
  startLoad();
  setInterval(startLoad,4000)


  // TODO: loading animation
  // TODO: change two sided chart colors
  // TODO: hover for information

  return (
    <div className="App">
      {!showResult && !isLoading &&
      <header className="App-header">
        <div className="title">Review Visualizer</div>
        <div className="subtitle">Presenting concise product review insights through data visualization.</div>
        <br/>
        <Search inputValue={inputValue}
                onChange={searchOnChange}
                onSubmit={submitForm}/>

      </header>
      }
      {isLoading &&
        <div className='loading-container'>
          <div className='loading-rotater'>
            <svg className="loading-svg" width="50" height="50" fill="transparent">
              <circle cx="25" cy="25" r="24" stroke="black"></circle>
            </svg>
          </div>
          <p className="loading-text">loading...</p>
        </div>
      }
      {showResult && !isLoading &&
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

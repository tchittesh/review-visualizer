import React, { useState, useEffect } from 'react';
import './App.css';
import Search from './components/search-bar.js'
import DoubleChart from './components/two-sided-chart.js';
import { FiHeart } from 'react-icons/fi'
const request = require('request');

function App() {
  const [inputValue, setInputValue] = useState("");
  const [showResult, setShowResult] = useState(false);

  function searchOnChange(event) {
    event.preventDefault();
    setInputValue(event.target.value);
  }

  function submitForm(event) {
    event.preventDefault();
    alert('search query submitted! ' + inputValue);

    // make request to the backend endpoint
    request.get({
      url: 'http://127.0.0.1:5000/visualize?product_name=' + inputValue
    }, function (err, httpResponse, body) {
      if (err) {
        alert(err);
      }
      console.log(body);

      setShowResult(true);
    })


  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="title">Review Visualizer</div>
        <div className="subtitle">Presenting concise product review insights through data visualization.</div>
        <br/>
        <Search inputValue={inputValue}
                onChange={searchOnChange}
                onSubmit={submitForm}/>


      </header>
      {showResult &&
        <DoubleChart
          vnegative={2}
          negative={1}
          snegative={2}
          spositive={5}
          positive={5}
          vpositive={5}
        />
      }
      <footer>
        Made with <FiHeart/> for HackMIT 2020. <a href="https://github.com/tchittesh/review-visualizer">View on Github</a>
      </footer>

    </div>
  );
}

export default App;

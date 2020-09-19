import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import Search from './components/search-bar.js'
import { FiHeart } from 'react-icons/fi'

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
    // and here is where we would make the request


    setShowResult(true);
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
        {showResult &&
          <div>Your query was submitted! Here is your data</div>
        }

      </header>
      <footer>
        Made with <FiHeart/> for HackMIT 2020. <a href="https://github.com/tchittesh/review-visualizer">View on Github</a>
      </footer>

    </div>
  );
}

export default App;

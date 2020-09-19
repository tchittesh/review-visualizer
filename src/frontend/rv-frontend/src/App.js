import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import Search from './components/search-bar.js'

function App() {
  const [inputValue, setInputValue] = useState("Search here");
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
        Review Visualizer
        <br/>
        <Search inputValue={inputValue}
                onChange={searchOnChange}
                onSubmit={submitForm}/>
        {showResult &&
          <div>Your query was submitted! Here is your data</div>
        }
      </header>
    </div>
  );
}

export default App;

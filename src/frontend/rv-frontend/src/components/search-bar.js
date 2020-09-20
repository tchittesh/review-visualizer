import React from 'react';
import { BsSearch } from 'react-icons/bs';
import '../css/search-bar.css';

function Search(props) {
  return (
    <div className="searchbar-wrapper">
      <form onSubmit={props.onSubmit}>
        <label htmlFor="search"><BsSearch/> </label>
        <input className="searchbar" type="text" value={props.inputValue} placeholder="Search for a product..." onChange={props.onChange}/>
      </form>
    </div>
  );
}

export default Search;

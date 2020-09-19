import React from 'react';

function Search(props) {
  return (
    <form onSubmit={props.onSubmit}>
      <label htmlFor="search">Search here </label>
      <input type="text" value={props.inputValue} onChange={props.onChange}/>
    </form>
  );
}

export default Search;

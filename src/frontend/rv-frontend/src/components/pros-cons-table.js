import React from 'react';
import '../css/pros-cons-table.css';

function ProsConsTable(props) {

  let pros = props.pros;
  let cons = props.cons;

  function get_safe(array, index) {
    if (index < array.length) return array[index];
    else return "_";
  }

  return (
    <table>
      <tbody>
        <tr>
          <th>Pros</th>
          <th>Cons</th>
        </tr>
        <tr>
          <td>{get_safe(pros, 0)}</td>
          <td>{get_safe(cons, 0)}</td>
        </tr>
        <tr>
          <td>{get_safe(pros, 1)}</td>
          <td>{get_safe(cons, 1)}</td>
        </tr>
        <tr>
          <td>{get_safe(pros, 2)}</td>
          <td>{get_safe(cons, 2)}</td>
        </tr>
      </tbody>
    </table>
  )
}

export default ProsConsTable;

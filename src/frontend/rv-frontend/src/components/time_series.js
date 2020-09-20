import React, { useEffect } from 'react';
import * as d3 from 'd3';
import '../css/time_series.css'


// inspired by code here https://bl.ocks.org/d3noob/402dd382a51a4f6eea487f9a35566de0
function TimeSeries(props) {

  // set the dimensions and margins of the graph
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

  // parse the date / time
  var parseTime = d3.timeParse("%Y-%m-%d");

  // set the ranges
  var x = d3.scaleTime().range([0, width]);
  var y = d3.scaleLinear().range([height, 0]);

  // define the line
  var valueline = d3.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.value); });


  useEffect(() => {
    // append the svg obgect to the body of the page
    // appends a 'group' element to 'svg'
    // moves the 'group' element to the top left margin

    var svg = d3.select("#time-series-svg").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    // Get the data

    let data = props.input;

    // format the data
    data.forEach(function(d) {
        if (typeof d.date === 'string') {
          d.date = parseTime(d.date);
        }
        d.value = +d.value;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.value; })]);

    // Add the valueline path.
    svg.append("path")
        .data([data])
        .attr("class", "line")
        .attr("d", valueline);

    // Add the X Axis
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add the Y Axis
    svg.append("g")
        .call(d3.axisLeft(y));

    return () => {
      // clear out the element
      document.getElementById('time-series-svg').innerHTML = "";
    }

  }, [props]);

  return (
    <div className="time-series-svg-wrapper">
      <div id="time-series-svg"></div>
    </div>
  )
}

export default TimeSeries;

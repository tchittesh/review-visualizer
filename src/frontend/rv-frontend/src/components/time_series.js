import React, { useEffect } from 'react';
import * as d3 from 'd3';
import '../css/time_series.css'


// inspired by code here https://bl.ocks.org/d3noob/402dd382a51a4f6eea487f9a35566de0
// https://bl.ocks.org/alandunning/cfb7dcd7951826b9eacd54f0647f48d3
function TimeSeries(props) {

  // set the dimensions and margins of the graph
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      //width = 960 - margin.left - margin.right,
      //height = 500 - margin.top - margin.bottom;
      width = 800 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;


  // parse the date / time
  var parseTime = d3.timeParse("%Y-%m-%d");

  function getDay(d) {
    if (d) {
      return d.date;
    } else {
      return 0;
    }
  }

  var bisectDate = d3.bisector(function(d) { return getDay(d); }).left;

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
    //y.domain([0, d3.max(data, function(d) { return d.value; })]);
    y.domain([0, 5])

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

    let focus = svg.append("g")
        .attr("class", "focus")
        .style("display", "none");

    focus.append("line")
        .attr("class", "x-hover-line hover-line")
        .attr("y1", 0)
        .attr("y2", height);

    focus.append("line")
        .attr("class", "y-hover-line hover-line")
        .attr("x1", width)
        .attr("x2", width);

    focus.append("circle")
        .attr("r", 7.5);

    focus.append("text")
        .attr("class", "text-desc")
        .attr("x", 15)
        .attr("dy", ".31em");


    svg.append("rect")
        //.attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .attr("class", "overlay")
        .attr("width", width)
        .attr("height", height)
        .on("mouseover", function() { focus.style("display", null); })
        .on("mouseout", function() { focus.style("display", "none"); })
        .on("mousemove", mousemove);


    function mousemove(event) {
      var x0 = x.invert(d3.pointer(event)[0]),
          i = bisectDate(data, x0, 1),
          d0 = data[i - 1],
          d1 = data[i],
          //d = x0 - d0.year > d1.year - x0 ? d1 : d0;
          d = x0 - getDay(d0) > getDay(d1) - x0 ? d1 : d0
      focus.attr("transform", "translate(" + x(d.date) + "," + y(d.value) + ")");
      focus.select("text").text(function() { return `Avg. star rating before ${d.date.toString().substr(0,15)}: ${d.value.toFixed(2)}`; });
      focus.select(".x-hover-line").attr("y2", height - y(d.value));
      focus.select(".y-hover-line").attr("x2", width + width);
    }

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

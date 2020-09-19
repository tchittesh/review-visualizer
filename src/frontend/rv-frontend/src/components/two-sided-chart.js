import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

// diverging chart based on demo here: https://observablehq.com/@d3/diverging-stacked-bar-chart
function DoubleChart(props) {

  const width = 700

  function getData() {


    const defaultName = "Product"
    let data = [
      {name: defaultName, category: "Very negative", value: props.vnegative},
      {name: defaultName, category: "Negative", value: props.negative},
      //{name: defaultName, category: "Slightly negative", value: props.snegative},
      //{name: defaultName, category: "Slightly positive", value: props.spositive},
      {name: defaultName, category: "Positive", value: props.positive},
      {name: defaultName, category: "Very positive", value: props.vpositive}
    ]

    // Normalize absolute values to percentage.

    d3.rollup(data, group => {
      const sum = d3.sum(group, d => d.value);
      for (const d of group) d.value /= sum;
    }, d => d.name);


    return Object.assign(data, {
      format: ".0%",
      negative: "← More negative keywords",
      positive: "More positive keywords →",
      negatives: ["Very negative", "Negative"],
      positives: ["Positive", "Very positive"]
    });
  }
  const data = getData()
  //console.log(data)

  const signs = new Map([].concat(
    data.negatives.map(d => [d, -1]),
    data.positives.map(d => [d, +1])
  ))

  const margin = ({top: 40, right: 30, bottom: 0, left: 80})

  const series = d3.stack()
    .keys([].concat(data.negatives.slice().reverse(), data.positives))
    .value(([, value], category) => signs.get(category) * (value.get(category) || 0))
    .offset(d3.stackOffsetDiverging)
  (d3.rollups(data, data => d3.rollup(data, ([d]) => d.value, d => d.category), d => d.name))

  const bias = d3.rollups(data, v => d3.sum(v, d => d.value * Math.min(0, signs.get(d.category))), d => d.name)
  .sort(([, a], [, b]) => d3.ascending(a, b))

  const height = bias.length * 33 + margin.top + margin.bottom

  const x = d3.scaleLinear()
    .domain(d3.extent(series.flat(2)))
    .rangeRound([margin.left, width - margin.right]);

  const y = d3.scaleBand()
    .domain(bias.map(([name]) => name))
    .rangeRound([margin.top, height - margin.bottom])
    .padding(2 / 33)

  const color = d3.scaleOrdinal()
    .domain([].concat(data.negatives, data.positives))
    .range(d3.schemeSpectral[data.negatives.length + data.positives.length])

  function formatValue(x) {
    const format = d3.format(data.format || "");
    return format(Math.abs(x));
  }

  let yAxis = g => g
    .call(d3.axisLeft(y).tickSizeOuter(0))
    .call(g => g.selectAll(".tick").data(bias).attr("transform", ([name, min]) => `translate(${x(min)},${y(name) + y.bandwidth() / 2})`))
    .call(g => g.select(".domain").attr("transform", `translate(${x(0)},0)`))

  let xAxis = g => g
    .attr("transform", `translate(0,${margin.top})`)
    .call(d3.axisTop(x)
        .ticks(width / 80)
        .tickFormat(formatValue)
        .tickSizeOuter(0))
    .call(g => g.select(".domain").remove())
    .call(g => g.append("text")
        .attr("x", x(0) + 20)
        .attr("y", -24)
        .attr("fill", "currentColor")
        .attr("text-anchor", "start")
        .text(data.positive))
    .call(g => g.append("text")
        .attr("x", x(0) - 20)
        .attr("y", -24)
        .attr("fill", "currentColor")
        .attr("text-anchor", "end")
        .text(data.negative))

  function drawChart() {

    const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height]);

    svg.append("g")
      .selectAll("g")
      .data(series)
      .join("g")
        .attr("fill", d => color(d.key))
      .selectAll("rect")
      .data(d => d.map(v => Object.assign(v, {key: d.key})))
      .join("rect")
        .attr("x", d => x(d[0]))
        .attr("y", ({data: [name]}) => y(name))
        .attr("width", d => x(d[1]) - x(d[0]))
        .attr("height", y.bandwidth())
      .append("title")
        .text(({key, data: [name, value]}) => `${name}
        ${formatValue(value.get(key))} ${key}`);

    svg.append("g")
      .call(xAxis);

    svg.append("g")
      .call(yAxis);

    return svg.node();
  }
  const chart = drawChart();

  const svg = useRef(null);
  useEffect(() => {
    if (svg.current) {
      svg.current.appendChild(chart);
    }
  });

  return (
    <div ref={svg}></div>
  );
}

export default DoubleChart;

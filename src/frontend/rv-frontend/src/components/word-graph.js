import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

// based on demo here: https://observablehq.com/@pjayathissa/disjoint-labeled-force-directed-graph
function WordGraph(props) {

  let keywords = props.graph.keywords;
  let keyword_valences = props.graph.keyword_valences;
  let keyword_pair_probabilities = props.graph.keyword_pair_probabilities;
  let keyword_frequencies = props.graph.keyword_frequencies;

  // normalize everything
  let minimum = Math.min(...Object.values(keyword_frequencies));
  let maximum = Math.max(...Object.values(keyword_frequencies));
  if (minimum === maximum) {
    for (let keyword of keywords) {
      keyword_frequencies[keyword] = 0.5;
    }
  } else {
    for (let keyword of keywords) {
      keyword_frequencies[keyword] = (keyword_frequencies[keyword] - minimum) / (maximum - minimum);
    }
  }

  let nodes = keywords.map(keyword => ({
    id: keyword,
    valence: keyword_valences[keyword],
    size: 2 + Math.floor(5 * keyword_frequencies[keyword]),
  }));

  let links = [];
  // use top (2 * keywords.length) edges
  let probabilities = [];
  for (let keyword1 of keywords) {
    for (let keyword2 of keywords) {
      if (keyword1 === keyword2) {
        continue;
      }
      probabilities.push(keyword_pair_probabilities[keyword1][keyword2]);
    }
  }
  probabilities.sort((a, b) => b-a);
  let threshold = -1;
  if (2*keywords.length < probabilities.length) threshold = probabilities[2*keywords.length];
  for (let keyword1 of keywords) {
    for (let keyword2 of keywords) {
      if (keyword1 === keyword2) {
        continue;
      }
      if (keyword_pair_probabilities[keyword1][keyword2] > threshold) {
        links.push({
          source: keyword1,
          target: keyword2,
          value: 2,
        });
      }
    }
  }

  let data = [{
    "nodes": nodes,
    "links": links,
  }];

  let height = 400;
  let width = 680;

  let color = d => d3.interpolateRdYlGn((d.valence + 1)/2);

  let drag = simulation => {

    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
  }

  function drawChart() {
    // Styling Params
    const scale = 3;
    const textOffset = 5;

    const links = data[0].links.map(d => Object.create(d));

    const nodes = data[0].nodes.map(d => Object.create(d));
    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody())
        .force("x", d3.forceX())
        .force("y", d3.forceY());

    const svg = d3.create("svg")
        .attr("viewBox", [-width / 2, -height / 2, width, height]);

    const link = svg.append("g")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(links)
      .join("line")
        .attr("stroke-width", d => Math.sqrt(d.value));

      const node = svg.append("g")
      .selectAll(".node")
      .data(nodes)
      .join("g")
      .attr("class", "node")
        .call(drag(simulation));


      const circle = node.append("circle")
          .attr("r", d => d.size)
          .attr("fill", color)
          .call(drag(simulation));



    const text = node.append("text")
        .text(d => d.id)
        .attr("font-size", d => `${Math.floor(keyword_frequencies[d.id] * 5 + 8)}px`);

    simulation.on("tick", () => {
      link
          .attr("x1", d => d.source.x*scale)
          .attr("y1", d => d.source.y*scale)
          .attr("x2", d => d.target.x*scale)
          .attr("y2", d => d.target.y*scale);
      text
          .attr("x", d => d.x*scale+textOffset)
          .attr("y", d => d.y*scale);

      circle
          .attr("cx", d => d.x*scale)
          .attr("cy", d => d.y*scale);
    });

    // invalidation.then(() => simulation.stop());

    return svg.node();
  }
  let chart = drawChart();

  const svg = useRef(null);
  useEffect(() => {
    if (svg.current) {
      svg.current.appendChild(chart);
    }
    return () => {
      svg.current.removeChild(chart);
    }
  }, [props]);

  return (
    <div style={{gridArea: '2/1/2/1'}} ref={svg}></div>
  )
}

export default WordGraph;

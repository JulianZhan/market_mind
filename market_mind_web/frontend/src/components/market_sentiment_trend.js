import React from "react";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

const AlphaVantageTrend = ({ data, dataKey, title }) => {
  /**
   * This const as a function component that renders a line chart.
   * @Param {Array} data - An array of alpha vantage data.
   * @Param {String} dataKey - The data key of the line chart.
   * @Param {String} title - The title of the line chart.
   * @Return {Component} - A line chart component consisting of a title and a line chart with html styling.
   */
  return (
    <div style={{ textAlign: "center" }}>
      <h3>{title}</h3>
      <LineChart width={550} height={300} data={data}>
        <Line type="monotone" dataKey={dataKey} stroke="#8884d8" />
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="dateRecorded" />
        <YAxis label={{ value: "Score", angle: -90, position: "insideLeft" }} />
        <Tooltip />
      </LineChart>
    </div>
  );
};

export default AlphaVantageTrend;

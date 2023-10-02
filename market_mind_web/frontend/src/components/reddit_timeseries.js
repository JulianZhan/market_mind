import React from "react";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

const RedditTimeSeries = ({ data, dataKey, title }) => {
  return (
    <div>
      <h3>{title}</h3>
      <LineChart width={600} height={300} data={data}>
        <Line type="monotone" dataKey="anger" stroke="#00FF00" />
        <Line type="monotone" dataKey="disgust" stroke="#FF0000" />
        <Line type="monotone" dataKey="fear" stroke="#8884d8" />
        <Line type="monotone" dataKey="joy" stroke="#0000FF" />
        <Line type="monotone" dataKey="sadness" stroke="#FFFF00" />
        <Line type="monotone" dataKey="surprise" stroke="#00FFFF" />
        <Line type="monotone" dataKey="neutral" stroke="#FF00FF" />
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="dateRecorded" />
        <YAxis />
        <Tooltip />
      </LineChart>
    </div>
  );
};

export default RedditTimeSeries;

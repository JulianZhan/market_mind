import React from "react";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

const RedditTrend = ({ data, title }) => {
  return (
    <div style={{ textAlign: "center" }}>
      <h3>{title}</h3>
      <LineChart width={550} height={300} data={data}>
        <Line type="monotone" dataKey="anger" stroke="#FF7F11" />
        <Line type="monotone" dataKey="disgust" stroke="#0e3b43" />
        <Line type="monotone" dataKey="fear" stroke="#8884d8" />
        <Line type="monotone" dataKey="joy" stroke="#5BC0EB" />
        <Line type="monotone" dataKey="sadness" stroke="#65532F" />
        <Line type="monotone" dataKey="surprise" stroke="#357266" />
        <Line type="monotone" dataKey="neutral" stroke="#6FD08C" />
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="dateRecorded" />
        <YAxis />
        <Tooltip />
      </LineChart>
    </div>
  );
};

export default RedditTrend;

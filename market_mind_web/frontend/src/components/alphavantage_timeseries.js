import React from "react";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

const AlphaVantageTimeSeries = ({ data, dataKey, title }) => {
  return (
    <div>
      <h3>{title}</h3>
      <LineChart width={600} height={300} data={data}>
        <Line type="monotone" dataKey={dataKey} stroke="#8884d8" />
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="dateRecorded" />
        <YAxis />
        <Tooltip />
      </LineChart>
    </div>
  );
};

export default AlphaVantageTimeSeries;

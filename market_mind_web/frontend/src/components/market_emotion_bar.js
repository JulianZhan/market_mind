import React from "react";
import { Cell, XAxis, YAxis, Tooltip, BarChart, Bar } from "recharts";

function getBarColor(value) {
  const opacity = Math.min(1, value * 5); // Arbitrary multiplier to adjust redness
  return `rgba(91,192,235, ${opacity})`; // Using RGBA to control the redness based on opacity
}

const RedditBarChart = ({ data, title }) => {
  const dataArray = Object.entries(data)
    .map(([key, value]) => ({ emotion: key, value }))
    .filter((entry) => entry.emotion !== "dateRecorded")
    .sort((a, b) => b.value - a.value);

  return (
    <div style={{ textAlign: "center" }}>
      <h3>{title}</h3>
      <BarChart
        width={500}
        height={300}
        data={dataArray}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      >
        <XAxis
          dataKey="emotion"
          tick={{ fontSize: 10, angle: -45, textAnchor: "end" }}
        />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value">
          {dataArray.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={getBarColor(entry.value)} />
          ))}
        </Bar>
      </BarChart>
    </div>
  );
};

export default RedditBarChart;

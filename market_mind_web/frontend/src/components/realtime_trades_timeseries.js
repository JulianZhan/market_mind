import React from "react";
import { LineChart, CartesianGrid, XAxis, YAxis, Legend, Line } from "recharts";

const RealtimeTradesTimeSeries = ({
  data,
  minPrice,
  maxPrice,
  domainMargin,
}) => {
  const formaYAxixtTick = (tickValue) => {
    return tickValue.toFixed(3);
  };

  const formatXAxisTick = (timestamp) => {
    const date = new Date(timestamp);
    // format as MM:SS
    return `${String(date.getHours()).padStart(2, "0")}:${String(
      date.getMinutes()
    ).padStart(2, "0")}:${String(date.getSeconds()).padStart(2, "0")}`;
  };

  return (
    <div>
      <LineChart
        width={1000}
        height={250}
        data={data}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        isAnimationActive={false} // Disable animation
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="tradeTimestamp" tickFormatter={formatXAxisTick} />
        <YAxis
          domain={[minPrice - domainMargin, maxPrice + domainMargin]}
          tickFormatter={formaYAxixtTick}
          tick={{ fontSize: 12 }} // Smaller font size for the y-axis
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="price"
          stroke="#8884d8"
          activeDot={false} // Disable active dot
          dot={false}
        />
      </LineChart>
    </div>
  );
};

export default RealtimeTradesTimeSeries;

import React from "react";
import { LineChart, CartesianGrid, XAxis, YAxis, Legend, Line } from "recharts";

const RealtimeTradesTimeSeries = ({
  data,
  minPrice,
  maxPrice,
  domainMargin,
}) => {
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
        <XAxis dataKey="tradeTimestamp" />
        <YAxis domain={[minPrice - domainMargin, maxPrice + domainMargin]} />
        <Legend />
        <Line
          type="monotone"
          dataKey="price"
          stroke="#8884d8"
          activeDot={false} // Disable active dot
          dot={false}
        />
      </LineChart>

      {/* Volume Chart */}
      <LineChart
        width={1000}
        height={250}
        data={data}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        isAnimationActive={false} // Disable animation
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="tradeTimestamp" />
        <YAxis />
        <Legend />
        <Line
          type="monotone"
          dataKey="volume"
          stroke="#82ca9d"
          activeDot={false}
          dot={false}
        />
      </LineChart>
    </div>
  );
};

export default RealtimeTradesTimeSeries;

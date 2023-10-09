import React from "react";
import { utcToZonedTime } from "date-fns-tz";
import { LineChart, CartesianGrid, XAxis, YAxis, Legend, Line } from "recharts";

const RealtimeTradesTimeSeries = ({
  data,
  minPrice,
  maxPrice,
  domainMargin,
}) => {
  const formaYAxixtTick = (tickValue) => {
    /**
     * This const as a function component that formats the y-axis tick.
     * It formats the tick value to 3 decimal.
     *
     * @Param {Number} tickValue - The value of the tick.
     * @Return {String} - A formatted string of the tick value.
     */
    return tickValue.toFixed(3);
  };

  const formatXAxisTick = (timestamp) => {
    /**
     * This const as a function component that formats the x-axis tick.
     * It formats the tick value to HH:MM:SS.
     *
     * @Param {Number} timestamp - The timestamp of the tick.
     * @Return {String} - A formatted string of the tick value.
     */
    let date = new Date(timestamp);
    // Get the user's timezone
    const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    // Convert the date to the user's timezone
    date = utcToZonedTime(date, userTimeZone);
    return `${String(date.getHours()).padStart(2, "0")}:${String(
      date.getMinutes()
    ).padStart(2, "0")}:${String(date.getSeconds()).padStart(2, "0")}`;
  };

  return (
    <div>
      {/**
       * The LineChart component is a recharts component that renders a line chart.
       * Due to the reason that we are rendering a real-time chart and updating the chart every second,
       * We minimize the level of interactivity to improve performance.
       */}
      <LineChart
        width={1000}
        height={250}
        data={data}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        isAnimationActive={false}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="tradeTimestamp" tickFormatter={formatXAxisTick} />
        <YAxis
          domain={[minPrice - domainMargin, maxPrice + domainMargin]}
          tickFormatter={formaYAxixtTick}
          tick={{ fontSize: 12 }}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="price"
          stroke="#8884d8"
          activeDot={false}
          dot={false}
        />
      </LineChart>
    </div>
  );
};

export default RealtimeTradesTimeSeries;

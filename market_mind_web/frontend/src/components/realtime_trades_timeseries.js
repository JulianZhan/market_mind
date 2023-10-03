import React, { useState, useEffect } from "react";
import SockJS from "sockjs-client";
import { Client } from "@stomp/stompjs";
import { LineChart, CartesianGrid, XAxis, YAxis, Legend, Line } from "recharts";

function RealtimeTradesTimeSeries() {
  const [data, setData] = useState([]);
  const [granularity, setGranularity] = useState(5);

  useEffect(() => {
    const socket = new SockJS("http://localhost:8080/websocket-endpoint");
    const stompClient = new Client({
      webSocketFactory: () => socket,
      onConnect: () => {
        stompClient.subscribe("/topic/trades", (message) => {
          const rawData = JSON.parse(message.body);
          setData(rawData);
        });
      },
    });
    stompClient.activate();

    return () => {
      if (stompClient.connected) {
        stompClient.deactivate();
      }
    };
  }, [granularity]);

  // Find min and max price to set the Y-axis domain
  const minPrice = Math.min(...data.map((item) => item.price));
  const maxPrice = Math.max(...data.map((item) => item.price));
  const domainMargin = (maxPrice - minPrice) * 0.05;

  const changeGranularity = async (e) => {
    const newGranularity = parseInt(e.target.value);
    setGranularity(newGranularity);
    // Call API to set granularity on server-side
    await fetch("http://localhost:8080/api/granularity", {
      method: "POST",
      body: new URLSearchParams({ granularity: newGranularity }),
    });
  };

  return (
    <div>
      <select value={granularity} onChange={changeGranularity}>
        <option value="1">1 Second</option>
        <option value="5">5 Seconds</option>
        <option value="60">1 Minute</option>
      </select>
      {/* Price Chart */}
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
}

export default RealtimeTradesTimeSeries;

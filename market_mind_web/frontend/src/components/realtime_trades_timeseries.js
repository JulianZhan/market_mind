import React, { useState, useEffect } from "react";
import SockJS from "sockjs-client";
import { Client } from "@stomp/stompjs";
import { LineChart, CartesianGrid, XAxis, YAxis, Legend, Line } from "recharts";

function RealtimeTradesTimeSeries() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const socket = new SockJS("http://localhost:8080/websocket-endpoint");
    const stompClient = new Client({
      webSocketFactory: () => socket,
      onConnect: () => {
        stompClient.subscribe("/topic/last-30-minutes", (message) => {
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
  }, []);

  // Find min and max price to set the Y-axis domain
  const minPrice = Math.min(...data.map((item) => item.price));
  const maxPrice = Math.max(...data.map((item) => item.price));
  const domainMargin = (maxPrice - minPrice) * 0.05; // Setting a 5% margin for clarity. Adjust if needed.

  return (
    <div>
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

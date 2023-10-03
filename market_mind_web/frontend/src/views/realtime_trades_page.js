import React, { useState, useEffect } from "react";
import RealtimeTradesTimeSeries from "../components/realtime_trades_timeseries";
import {
  initiateWebSocketConnection,
  updateGranularityOnServer,
} from "../api/realtime_trades_dashboard";

function RealtimeTradesPage() {
  const [data, setData] = useState([]);
  const [granularity, setGranularity] = useState(5);

  useEffect(() => {
    const stompClient = initiateWebSocketConnection(setData);

    return () => {
      if (stompClient.connected) {
        stompClient.deactivate();
      }
    };
  }, [granularity]);

  const minPrice = Math.min(...data.map((item) => item.price));
  const maxPrice = Math.max(...data.map((item) => item.price));
  const domainMargin = (maxPrice - minPrice) * 0.05;

  const changeGranularity = async (e) => {
    const newGranularity = parseInt(e.target.value);
    setGranularity(newGranularity);
    await updateGranularityOnServer(newGranularity);
  };

  return (
    <div>
      <h1>BTC Price</h1>
      <select value={granularity} onChange={changeGranularity}>
        <option value="1">1 Second</option>
        <option value="5">5 Seconds</option>
        <option value="60">1 Minute</option>
      </select>
      <RealtimeTradesTimeSeries
        data={data}
        minPrice={minPrice}
        maxPrice={maxPrice}
        domainMargin={domainMargin}
      />
    </div>
  );
}

export default RealtimeTradesPage;

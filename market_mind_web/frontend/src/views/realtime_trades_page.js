import React, { useState, useEffect } from "react";
import RealtimeTradesTimeSeries from "../components/realtime_trades_timeseries";
import {
  initiateWebSocketConnection,
  updateGranularityOnServer,
} from "../api/realtime_trades_dashboard";
import { Link } from "react-router-dom";

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
  const domainMargin = (maxPrice - minPrice) * 0.1;

  const changeGranularity = async (e) => {
    const newGranularity = parseInt(e.target.value);
    setGranularity(newGranularity);
    await updateGranularityOnServer(newGranularity);
  };

  return (
    (document.title = "Market Mind"),
    (
      <div className="container mt-4">
        <div className="row mb-4">
          <div className="col-md-6">
            <h1>BTC Price</h1>
            <p>View real-time BTC prices with various granularities.</p>
          </div>
          <div className="col-md-6 d-flex align-items-center">
            <select
              className="form-control"
              value={granularity}
              onChange={changeGranularity}
            >
              <option value="1">1 Second</option>
              <option value="5">5 Seconds</option>
              <option value="60">1 Minute</option>
            </select>
            <Link to="/">
              <button className="btn btn-secondary -3">Back to Home</button>{" "}
            </Link>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <RealtimeTradesTimeSeries
              data={data}
              minPrice={minPrice}
              maxPrice={maxPrice}
              domainMargin={domainMargin}
            />
          </div>
        </div>
      </div>
    )
  );
}

export default RealtimeTradesPage;

import React, { useState, useEffect } from "react";
import RealtimeTradesTimeSeries from "../components/realtime_trades_timeseries";
import {
  initiateWebSocketConnection,
  updateGranularityOnServer,
} from "../api/realtime_trades_dashboard";
import { Link } from "react-router-dom";

function RealtimeTradesPage() {
  /**
   * Use useState to define setter for variables and init them with empty or default values.
   */
  const [data, setData] = useState([]);
  const [granularity, setGranularity] = useState(5); // default to 5 seconds
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    /**
     * Use useEffect to fetch data from backend API and render to browser.
     * When granularity changes, useEffect will be triggered.
     * After triggering, it will re-initiate the websocket connection and update the granularity on the server.
     */

    // initiate websocket connection, pass setData as the callback function
    const stompClient = initiateWebSocketConnection(setData, () =>
      setIsLoading(false)
    );
    // update granularity on the server
    updateGranularityOnServer(granularity);

    /**
     * This is a cleanup function that will be executed when the granularity changes.
     * It will deactivate the stomp client.
     */
    return () => {
      if (stompClient.connected) {
        stompClient.deactivate();
      }
    };
  }, [granularity]);

  // get the min and max price from the data array to make the chart more readable
  const minPrice = Math.min(...data.map((item) => item.price));
  const maxPrice = Math.max(...data.map((item) => item.price));
  const domainMargin = (maxPrice - minPrice) * 0.1;

  /**
   * This function is executed when the granularity is changed.
   * It will update the granularity state and update the granularity on the server.
   * @Param {Event} e - The event object.
   */
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
            <h1>Bitcoin Price</h1>
            <p>
              View realtime Bitcoin prices with various granularities at
              Coinbase exchange.
            </p>
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
          </div>
        </div>
        <div className="row">
          <div className="col">
            {isLoading ? (
              <div className="loading">
                <p>Establishing connection...</p>
              </div>
            ) : (
              <RealtimeTradesTimeSeries
                data={data}
                minPrice={minPrice}
                maxPrice={maxPrice}
                domainMargin={domainMargin}
              />
            )}
            <div className="text-center mt-4">
              <Link to="/" className="btn btn-primary btn-lg">
                Back to Home
              </Link>
            </div>
          </div>
        </div>
      </div>
    )
  );
}

export default RealtimeTradesPage;

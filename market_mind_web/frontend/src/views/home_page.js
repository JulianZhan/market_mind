import React, { useState, useEffect } from "react";
import {
  fetchAlphaVantageData,
  fetchRedditData,
} from "../api/market_sentiment";
import AlphaVantageTimeSeries from "../components/alphavantage_timeseries";
import RedditTimeSeries from "../components/reddit_timeseries";

const HomePage = () => {
  const [alphavantageData, setAlphaData] = useState([]);
  const [redditData, setRedditData] = useState([]);

  useEffect(() => {
    // Replace with your date range
    const startDate = "2023-01-01";
    const endDate = "2023-12-31";

    fetchAlphaVantageData(startDate, endDate).then((data) =>
      setAlphaData(data)
    );
    fetchRedditData(startDate, endDate).then((data) => setRedditData(data));
  }, []);

  return (
    <div>
      <AlphaVantageTimeSeries
        data={alphavantageData}
        dataKey="avgScore"
        title="Alpha Vantage Data"
      />
      <RedditTimeSeries
        data={redditData}
        dataKey="avgScore"
        title="Reddit Data"
      />
    </div>
  );
};

export default HomePage;

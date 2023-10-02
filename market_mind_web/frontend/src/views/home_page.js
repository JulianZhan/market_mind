import React, { useState, useEffect } from "react";
import {
  fetchAlphaVantageData,
  fetchRedditData,
  fetchAlphaVantageMostRecent,
  fetchRedditMostRecent,
} from "../api/home_dashboard";
import AlphaVantageTrend from "../components/market_sentiment_trend";
import RedditTrend from "../components/market_emotion_trend";
import RedditBarChart from "../components/market_emotion_bar";

const HomePage = () => {
  const [alphavantageData, setAlphaData] = useState([]);
  const [redditData, setRedditData] = useState([]);
  const [redditBarData, setRedditBarData] = useState([]);

  useEffect(() => {
    // Replace with your date range
    const startDate = "2023-01-01";
    const endDate = "2023-12-31";

    fetchAlphaVantageData(startDate, endDate).then((data) =>
      setAlphaData(data)
    );
    fetchRedditData(startDate, endDate).then((data) => setRedditData(data));
    fetchRedditMostRecent().then((data) => setRedditBarData(data));
  }, []);

  return (
    <div>
      <AlphaVantageTrend
        data={alphavantageData}
        dataKey="avgScore"
        title="Market Sentiment"
      />
      <RedditTrend data={redditData} title="Market Emotion" />
      <RedditBarChart data={redditBarData} title="Market Emotion" />
    </div>
  );
};

export default HomePage;

import React, { useState, useEffect } from "react";
import {
  fetchAlphaVantageData,
  fetchRedditData,
  fetchAlphaVantageMostRecent,
  fetchRedditMostRecent,
} from "../api/home_dashboard";
import AlphaVantageTrend from "../components/market_sentiment_trend";
import AlphaVantageStat from "../components/market_sentiment_stat";
import RedditTrend from "../components/market_emotion_trend";
import RedditBarChart from "../components/market_emotion_bar";

const HomePage = () => {
  const [alphavantageData, setAlphaData] = useState([]);
  const [alphavantageStatData, setAlphaStatData] = useState([]);
  const [redditData, setRedditData] = useState([]);
  const [redditBarData, setRedditBarData] = useState([]);
  const [selectedEndDate, setSelectedEndDate] = useState(new Date()); // default to today
  const [timeLength, setTimeLength] = useState(7); // default to 7 days

  useEffect(() => {
    const startDate = new Date(selectedEndDate);
    startDate.setDate(startDate.getDate() - timeLength);

    fetchAlphaVantageData(
      startDate.toISOString().split("T")[0],
      selectedEndDate.toISOString().split("T")[0]
    ).then((data) => setAlphaData(data));
    fetchAlphaVantageMostRecent().then((data) => setAlphaStatData(data));

    fetchRedditData(
      startDate.toISOString().split("T")[0],
      selectedEndDate.toISOString().split("T")[0]
    ).then((data) => setRedditData(data));
    fetchRedditMostRecent().then((data) => setRedditBarData(data));
  }, [selectedEndDate, timeLength]);

  return (
    <div>
      <div>
        {/* Date Picker */}
        <input
          type="date"
          value={selectedEndDate.toISOString().split("T")[0]}
          onChange={(e) => setSelectedEndDate(new Date(e.target.value))}
        />

        {/* Time Length Dropdown */}
        <select
          value={timeLength}
          onChange={(e) => setTimeLength(Number(e.target.value))}
        >
          <option value={7}>7 days</option>
          <option value={14}>14 days</option>
        </select>
      </div>
      <AlphaVantageTrend
        data={alphavantageData}
        dataKey="avgScore"
        title="Market Sentiment"
      />
      <AlphaVantageStat data={alphavantageStatData} />
      <RedditTrend data={redditData} title="Market Emotion" />
      <RedditBarChart data={redditBarData} title="Market Emotion" />
    </div>
  );
};

export default HomePage;

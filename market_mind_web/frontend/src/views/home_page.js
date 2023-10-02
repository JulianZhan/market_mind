import React, { useState, useEffect } from "react";
import { fetchAlphaVantageData, fetchRedditData } from "../api/home_dashboard";
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
    let startDate = new Date(selectedEndDate);
    startDate.setDate(startDate.getDate() - timeLength);
    startDate = startDate.toISOString().split("T")[0];
    const formattedEndDate = selectedEndDate.toISOString().split("T")[0];

    fetchAlphaVantageData(startDate, formattedEndDate).then((data) =>
      setAlphaData(data)
    );
    fetchAlphaVantageData(formattedEndDate, formattedEndDate).then((data) =>
      setAlphaStatData(data.length > 0 ? data[0] : [])
    );

    fetchRedditData(startDate, formattedEndDate).then((data) =>
      setRedditData(data)
    );
    fetchRedditData(formattedEndDate, formattedEndDate).then((data) =>
      setRedditBarData(data.length > 0 ? data[0] : [])
    );
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

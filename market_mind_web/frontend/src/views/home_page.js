import React, { useState, useEffect } from "react";
import { Client } from "@stomp/stompjs";
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
import RealtimeTradesTimeSeries from "../components/realtime_trades_timeseries";

const HomePage = () => {
  const [alphavantageData, setAlphaData] = useState([]);
  const [alphavantageStatData, setAlphaStatData] = useState([]);
  const [redditData, setRedditData] = useState([]);
  const [redditBarData, setRedditBarData] = useState([]);
  const [tradesData, setTradesData] = useState([]);

  useEffect(() => {
    // Replace with your date range
    const startDate = "2023-01-01";
    const endDate = "2023-12-31";

    fetchAlphaVantageData(startDate, endDate).then((data) =>
      setAlphaData(data)
    );
    fetchAlphaVantageMostRecent().then((data) => setAlphaStatData(data));
    fetchRedditData(startDate, endDate).then((data) => setRedditData(data));
    fetchRedditMostRecent().then((data) => setRedditBarData(data));

    // WebSocket setup
    const socket = new Client({
      brokerURL: "http://localhost:8080/websocket-endpoint",
      debug: (str) => console.log(str),
      reconnectDelay: 5000,
      heartbeatIncoming: 4000,
      heartbeatOutgoing: 4000,
    });

    socket.onConnect = (frame) => {
      socket.subscribe("/topic/last-30-minutes", (message) => {
        setTradesData(JSON.parse(message.body));
      });
    };

    return () => {
      socket.deactivate();
    };
  }, []);

  return (
    <div>
      <AlphaVantageTrend
        data={alphavantageData}
        dataKey="avgScore"
        title="Market Sentiment"
      />
      <AlphaVantageStat data={alphavantageStatData} />
      <RedditTrend data={redditData} title="Market Emotion" />
      <RedditBarChart data={redditBarData} title="Market Emotion" />
      <RealtimeTradesTimeSeries data={tradesData} />
    </div>
  );
};

export default HomePage;

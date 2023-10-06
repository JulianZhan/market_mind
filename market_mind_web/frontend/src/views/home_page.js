import React, { useState, useEffect } from "react";
import { fetchAlphaVantageData, fetchRedditData } from "../api/home_dashboard";
import AlphaVantageTrend from "../components/market_sentiment_trend";
import AlphaVantageStat from "../components/market_sentiment_stat";
import RedditTrend from "../components/market_emotion_trend";
import RedditBarChart from "../components/market_emotion_bar";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Link } from "react-router-dom";

const HomePage = () => {
  const [alphavantageData, setAlphaData] = useState([]);
  const [alphavantageStatData, setAlphaStatData] = useState([]);
  const [redditData, setRedditData] = useState([]);
  const [redditBarData, setRedditBarData] = useState([]);
  const [selectedEndDate, setSelectedEndDate] = useState(new Date()); // default to today
  const [timeLength, setTimeLength] = useState(7); // default to 7 days

  useEffect(() => {
    let startDate = new Date(selectedEndDate);
    const utcDate = new Date(
      startDate.toLocaleString("en-US", { timeZone: "UTC" })
    );
    const formattedStartDate = utcDate.toISOString().split("T")[0];
    const formattedEndDate = selectedEndDate.toISOString().split("T")[0];

    fetchAlphaVantageData(formattedStartDate, formattedEndDate).then((data) =>
      setAlphaData(data)
    );
    fetchAlphaVantageData(formattedEndDate, formattedEndDate).then((data) =>
      setAlphaStatData(data.length > 0 ? data[0] : [])
    );

    fetchRedditData(formattedStartDate, formattedEndDate).then((data) =>
      setRedditData(data)
    );
    fetchRedditData(formattedEndDate, formattedEndDate).then((data) =>
      setRedditBarData(data.length > 0 ? data[0] : [])
    );
  }, [selectedEndDate, timeLength]);

  return (
    (document.title = "Market Mind"),
    (
      <div className="container mt-5">
        <div className="dashboard-header text-center mb-4">
          <h1>Market Mind</h1>
          <p>The latest market sentiment from news and reddit!</p>
          <Link to="/realtime-trades">
            <button className="btn btn-primary">
              Go to Real-time Dashboard
            </button>
          </Link>
        </div>

        <div className="mb-4">
          <div className="form-row">
            <div className="col">
              {/* Date Picker */}
              <p>Pick a Date!</p>
              <DatePicker
                selected={selectedEndDate}
                onChange={(date) => setSelectedEndDate(date)}
                dateFormat="yyyy-MM-dd"
              />
            </div>
            <div className="col">
              {/* Time Length Dropdown */}
              <p>Time Length</p>
              <select
                value={timeLength}
                onChange={(e) => setTimeLength(Number(e.target.value))}
              >
                <option value={7}>7 days</option>
                <option value={14}>14 days</option>
              </select>
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col-md-6 mb-4">
            <AlphaVantageTrend
              data={alphavantageData}
              dataKey="avgScore"
              title="Market Sentiment Trend"
            />
          </div>
          <div className="col-md-6 mb-4">
            <AlphaVantageStat
              data={alphavantageStatData}
              title="Market Sentiment"
            />
          </div>
          <div className="col-md-6 mb-4">
            <RedditTrend data={redditData} title="Market Emotion Trend" />
          </div>
          <div className="col-md-6 mb-4">
            <RedditBarChart data={redditBarData} title="Market Emotion" />
          </div>
        </div>
      </div>
    )
  );
};

export default HomePage;

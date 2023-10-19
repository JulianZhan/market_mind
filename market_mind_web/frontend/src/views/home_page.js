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
  /**
   * Use useState to define setter for variables and init them with empty or default values.
   */
  const [alphavantageData, setAlphaData] = useState([]);
  const [alphavantageStatData, setAlphaStatData] = useState([]);
  const [redditData, setRedditData] = useState([]);
  const [redditBarData, setRedditBarData] = useState([]);
  const [selectedEndDate, setSelectedEndDate] = useState(new Date()); // default to today
  const [timeLength, setTimeLength] = useState(7); // default to 7 days

  useEffect(() => {
    /**
     * Use useEffect to fetch data from backend API and render to browser.
     *
     * When selectedEndDate or timeLength changes, useEffect will be triggered.
     * After triggering, it will set the new data to the corresponding state.
     * and fetch data from backend API and render to browser.
     *
     * @Param {Date} selectedEndDate - The selected end date.
     * @Param {Number} timeLength - The time length.
     */
    let startDate = new Date(selectedEndDate);
    startDate.setDate(startDate.getDate() - timeLength);
    const utcStartDate = startDate.toISOString().split("T")[0];
    const utcEndDate = selectedEndDate.toISOString().split("T")[0];

    fetchAlphaVantageData(utcStartDate, utcEndDate).then((data) =>
      setAlphaData(data)
    );
    // if data is not empty, set the first item in the array as the data for the stat component
    fetchAlphaVantageData(utcEndDate, utcEndDate).then((data) =>
      setAlphaStatData(data.length > 0 ? data[0] : [])
    );

    fetchRedditData(utcStartDate, utcEndDate).then((data) =>
      setRedditData(data)
    );
    // if data is not empty, set the first item in the array as the data for the bar chart component
    fetchRedditData(utcEndDate, utcEndDate).then((data) =>
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
          {/* Link to Real-time Dashboard */}
          <Link to="/realtime-trades">
            <button className="btn btn-primary">
              Go to Realtime trades Dashboard
            </button>
          </Link>
          <Link to="/api-documentation">
            <button className="btn btn-secondary">API Documentation</button>
          </Link>
          <Link to="/about">
            <button className="btn btn-secondary">About</button>
          </Link>
        </div>

        {/* Bootstrap grid system */}
        <div className="mb-4">
          <div className="form-row">
            <div className="col">
              {/* Date Picker */}
              <p>Pick a Date!</p>
              <DatePicker
                selected={selectedEndDate}
                onChange={(date) => setSelectedEndDate(date)}
                dateFormat="yyyy-MM-dd"
                minDate={new Date("2023-10-10")}
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

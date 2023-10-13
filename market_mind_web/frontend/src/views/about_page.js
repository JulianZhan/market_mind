import React from "react";
import { Link } from "react-router-dom";

const AboutPage = () => {
  document.title = "Market Mind";

  return (
    <div className="container mt-5">
      <div className="text-center">
        <h1 className="display-4 mb-4">About Market Mind</h1>
      </div>

      <div className="card mb-4 shadow-sm">
        <div className="card-body">
          <p className="lead">
            Market Mind gives you a clear look into the cryptocurrency market,
            focusing on Bitcoin trades at Coinbase. We use AI to provide a
            comprehensive perspective on the crypto world. Below are our
            offerings:
          </p>
        </div>
      </div>

      <div className="card mb-4 shadow-sm">
        <div className="card-header">1. Market Sentiment Analysis:</div>
        <div className="card-body">
          <p>
            Market Mind sources data from Alpha Vantage, capturing live market
            news & sentiments globally. This data spans topics from
            cryptocurrency and stocks to fiscal policies. We provide a sentiment
            score reflecting the market's overall mood, ranging from -1 to 1.
          </p>
        </div>
      </div>

      <div className="card mb-4 shadow-sm">
        <div className="card-header">2. Market Emotions from Reddit:</div>
        <div className="card-body">
          <p>
            Gleaning from Reddit's 'cryptocurrency' subreddit, we harness
            insights and discussions. Our "emotion-english-distilroberta-base"
            model classifies emotions into 7 primary categories:
          </p>
          <ul className="list-group list-group-flush">
            <li className="list-group-item">
              <strong>Anger</strong>
            </li>
            <li className="list-group-item">
              <strong>Disgust</strong>
            </li>
            <li className="list-group-item">
              <strong>Fear</strong>
            </li>
            <li className="list-group-item">
              <strong>Joy</strong>
            </li>
            <li className="list-group-item">
              <strong>Neutral</strong>
            </li>
            <li className="list-group-item">
              <strong>Sadness</strong>
            </li>
            <li className="list-group-item">
              <strong>Surprise</strong>
            </li>
          </ul>
          <p className="mt-3">
            The score for each emotion varies between 0 and 1, indicating its
            intensity.
          </p>
        </div>
      </div>

      <div className="card mb-4 shadow-sm">
        <div className="card-header">3. Real-Time Trades Visualization:</div>
        <div className="card-body">
          <p>
            View live Bitcoin prices from Coinbase with selectable
            granularities, from per-second updates to per-minute overviews. Our
            live charts, bolstered by a WebSocket connection, enable traders to
            spot price changes instantly.
          </p>
        </div>
      </div>

      <div className="text-center mt-4">
        <Link to="/" className="btn btn-primary btn-lg">
          Back to Home
        </Link>
      </div>
    </div>
  );
};

export default AboutPage;

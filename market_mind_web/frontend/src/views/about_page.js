import React from "react";

const AboutPage = () => {
  return (
    <div className="container mt-5">
      <h2>About Market Mind</h2>
      <p>
        Market Mind is your trusted partner in understanding the intricate
        emotions and sentiments driving the cryptocurrency market, specifically
        focusing on Bitcoin trades at Coinbase. Here's a deeper dive into how we
        gather our insights:
      </p>

      <h3>1. Market Sentiment Analysis:</h3>
      <p>
        Our market sentiment is derived from Alpha Vantage's robust monitoring
        system that keenly observes market news and conducts a comprehensive
        sentiment analysis. By examining news articles, reports, and other
        media, we generate a sentiment score that reflects the market's current
        mood regarding Bitcoin. The score is a representation within a range of
        0 to 1, where a higher score indicates a more positive sentiment.
      </p>

      <h3>2. Market Emotion from Reddit:</h3>
      <p>
        Cryptocurrency enthusiasts, traders, and experts often flock to the
        'cryptocurrency' subreddit on Reddit to share their thoughts, insights,
        and feelings about the current market scenario. We tap into this rich
        source of qualitative data and employ the state-of-the-art model
        "emotion-english-distilroberta-base" to predict the prevalent market
        emotions. This model helps us categorize emotions into seven distinct
        types. Each emotion type's intensity is represented with a score between
        0 and 1.
      </p>

      <p>
        Through these methodologies, Market Mind provides real-time, insightful
        data to help traders and enthusiasts make informed decisions in the
        volatile world of cryptocurrency.
      </p>
    </div>
  );
};

export default AboutPage;

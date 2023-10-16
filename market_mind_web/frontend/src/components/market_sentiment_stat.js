import React from "react";

const AlphaVantageStat = ({
  data,
  title,
  rgbColorSentiment = "91,192,235",
}) => {
  /**
   * This const as a function component that renders a sentiment stat.
   * @Param {Array} data - An array of alpha vantage data.
   * @Param {String} title - The title of the sentiment stat.
   * @Param {String} rgbColorSentiment - The RGB color of the sentiment.
   * @Return {Component} - A sentiment stat component consisting of a title, sentiment and score with html styling.
   */

  // This function returns a title based on the average score.
  const getTitle = (avgScore) => {
    if (avgScore <= -0.35) return "Bearish";
    if (avgScore > -0.35 && avgScore <= -0.15) return "Somewhat-Bearish";
    if (avgScore > -0.15 && avgScore < 0.15) return "Neutral";
    if (avgScore >= 0.15 && avgScore < 0.35) return "Somewhat-Bullish";
    if (avgScore >= 0.35) return "Bullish";
    return ""; // should never reach here
  };

  const sentiment = getTitle(data?.avgScore);

  return (
    <div style={{ textAlign: "center" }}>
      {" "}
      {/* Centered content */}
      <h2>{title}</h2>
      <h1 style={{ color: `rgb(${rgbColorSentiment})`, fontSize: "4.5rem" }}>
        {sentiment}
      </h1>{" "}
      {/* Custom RGB color and larger text size for sentiment */}
      <h2 style={{ fontSize: "3.5rem" }}>
        <b>Score:</b> {data?.avgScore}
      </h2>{" "}
      {/* Different RGB color and larger text size for score */}
    </div>
  );
};

export default AlphaVantageStat;

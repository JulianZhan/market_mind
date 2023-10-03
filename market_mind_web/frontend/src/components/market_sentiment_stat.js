import React from "react";

const AlphaVantageStat = ({
  data,
  title,
  rgbColorSentiment = "91,192,235",
}) => {
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
      <h1 style={{ color: `rgb(${rgbColorSentiment})`, fontSize: "5rem" }}>
        {sentiment}
      </h1>{" "}
      {/* Custom RGB color and even larger text size for sentiment */}
      <h2 style={{ fontSize: "4rem" }}>
        <b>Score:</b> {data?.avgScore}
      </h2>{" "}
      {/* Different RGB color and even larger text size for score */}
    </div>
  );
};

export default AlphaVantageStat;

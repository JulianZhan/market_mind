import React from "react";

const AlphaVantageStat = ({ data, title }) => {
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
    <div>
      <h2>{title}</h2>
      <h3>{sentiment}</h3>
      <p>
        <b>Score:</b> {data?.avgScore}
      </p>
    </div>
  );
};

export default AlphaVantageStat;

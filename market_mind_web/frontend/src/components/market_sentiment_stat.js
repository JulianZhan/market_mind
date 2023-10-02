import React from "react";

const AlphaVantageStat = ({ data }) => {
  const getTitle = (avgScore) => {
    if (avgScore <= -0.35) return "Bearish";
    if (avgScore > -0.35 && avgScore <= -0.15) return "Somewhat-Bearish";
    if (avgScore > -0.15 && avgScore < 0.15) return "Neutral";
    if (avgScore >= 0.15 && avgScore < 0.35) return "Somewhat-Bullish";
    if (avgScore >= 0.35) return "Bullish";
    return ""; // should never reach here
  };
  const title = getTitle(data?.avgScore);

  return (
    <div>
      <h3>{title}</h3>
      <p>
        <b>Score:</b> {data?.avgScore}
      </p>
    </div>
  );
};

export default AlphaVantageStat;

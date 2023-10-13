const ApiDocumentation = ({ apiUrl, wsUrl }) => {
  return (
    <div>
      <h2>API Documentation</h2>
      <p>
        <strong>Server URL:</strong> {apiUrl} (HTTPS Supported)
      </p>

      {/* Market Sentiment */}
      <div className="api-section">
        <h3>/market_sentiment</h3>
        <p>
          <strong>Method:</strong> GET
        </p>
        <p>
          <strong>Description:</strong> Fetch market sentiment data for a
          specific date.
        </p>
        <p>
          <strong>Parameters:</strong>
        </p>
        <ul>
          <li>
            <code>date</code>: Target date in YYYY-MM-DD format (UTC).
          </li>
        </ul>
        <p>
          <strong>Sample Request:</strong>
        </p>
        <code>GET {apiUrl}/market_sentiment?date=2023-10-04</code>
        <p>
          <strong>Sample Response:</strong>
        </p>
        <pre>{`{
"data": {
"date_recorded": "2023-10-04",
"score": {
"avg_score": 0.144052,
"max_score": 0.628475,
"min_score": -0.598691,
"std_score": 0.166618
},
"score_definition": {
"Bearish": "score <= -0.35",
"Bullish": "score >= 0.35",
"Neutral": "-0.15 < score < 0.15",
"Somewhat-Bearish": "-0.35 < score <= -0.15",
"Somewhat-Bullish": "0.15 <= score < 0.35"
}
},
"message": "success"
}`}</pre>
      </div>

      {/* Market Emotion */}
      <div className="api-section">
        <h3>/market_emotion</h3>
        <p>
          <strong>Method:</strong> GET
        </p>
        <p>
          <strong>Description:</strong> Fetch market emotion data for a specific
          date.
        </p>
        <p>
          <strong>Parameters:</strong>
        </p>
        <ul>
          <li>
            <code>date</code>: Target date in YYYY-MM-DD format (UTC).
          </li>
        </ul>
        <p>
          <strong>Sample Request:</strong>
        </p>
        <code>GET {apiUrl}/market_emotion?date=2023-10-04</code>
        <p>
          <strong>Sample Response:</strong>
        </p>
        <pre>{`{
"data": {
"date_recorded": "2023-10-04",
"emotion": {
"anger": 0.101625,
"disgust": 0.0299405,
"fear": 0.0570223,
"joy": 0.147233,
"neutral": 0.383693,
"sadness": 0.112627,
"surprise": 0.167859
}
},
"message": "success"
}`}</pre>
      </div>

      {/* Real-time Data */}
      <div className="api-section">
        <h3>Real-time Data via WebSockets</h3>
        <p>
          <strong>Description:</strong> Receive real-time market trade data via
          WebSockets.
        </p>
        <p>
          Connect to the WebSocket and listen for the "market_trades" event to
          receive decoded Avro messages from the Kafka topic.
        </p>
        <p>
          <strong>Sample Request:</strong>
        </p>
        <code>WebSocket Connection to: {wsUrl}</code>
        <br />
        <code>Event to Listen: market_trades</code>
        <p>
          <strong>Sample WebSocket Response:</strong>
        </p>
        <pre>{`{
"data": {
"c": [1],
"ev": "XT",
"i": "568114041",
"p": 26789.01,
"pair": "BTC-USD",
"r": 1697170879996,
"s": 0.00388066,
"t": 1697170879990,
"x": 1
}
}`}</pre>
        <h4>Response Attributes:</h4>
        <ul>
          <li>
            <code>ev</code>: "XT": crypto tades
          </li>
          <li>
            <code>pair</code>: The crypto pair
          </li>
          <li>
            <code>p</code>: The price
          </li>
          <li>
            <code>t</code>: The Timestamp in Unix MS
          </li>
          <li>
            <code>s</code>: The size
          </li>
          <li>
            <code>c</code>: The conditions
            <ul>
              <li>0 (or empty array): empty</li>
              <li>1: sell side</li>
              <li>2: buy side</li>
            </ul>
          </li>
          <li>
            <code>i</code>: The ID of the trade (optional)
          </li>
          <li>
            <code>x</code>: 1: Coinbase
          </li>
          <li>
            <code>r</code>: The timestamp that the tick was received from source
          </li>
        </ul>
      </div>
    </div>
  );
};

export default ApiDocumentation;

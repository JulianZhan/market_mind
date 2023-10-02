// src/App.js

import React from "react";
import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./views/home_page";
import RealtimeTradesTimeSeries from "./views/realtime_trades_page";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/realtime-trades" element={<RealtimeTradesTimeSeries />} />
      </Routes>
    </Router>
  );
}

export default App;

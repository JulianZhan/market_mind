// src/App.js

import React from "react";
import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./views/home_page";
import RealtimeTradesTimeSeries from "./views/realtime_trades_page";
import ApiDocumentationPage from "./views/api_documentation_page";
import NotFound from "./views/notfound_page";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/realtime-trades" element={<RealtimeTradesTimeSeries />} />
        <Route path="/api-documentation" element={<ApiDocumentationPage />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;

import React from "react";
import { Link } from "react-router-dom";
import ApiDocumentation from "../components/api_documentation";

const ApiDocumentationPage = () => {
  const apiUrl = "https://api.market-mind-web.com"; // Added API server URL
  const wsUrl = "wss://api.market-mind-web.com"; // WebSocket URL

  return (
    (document.title = "Market Mind"),
    (
      <div>
        <div className="container mt-5">
          <ApiDocumentation apiUrl={apiUrl} wsUrl={wsUrl} />
          <div className="text-center mt-4">
            <Link to="/" className="btn btn-primary btn-md">
              Back to Home
            </Link>
          </div>
        </div>
      </div>
    )
  );
};

export default ApiDocumentationPage;

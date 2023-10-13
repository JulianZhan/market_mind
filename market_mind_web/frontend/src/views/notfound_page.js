import React from "react";
import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div>
      <h1>Not Found</h1>
      <p>Sorry, nothing here.</p>
      <Link to="/" className="btn btn-primary btn-md">
        Back to Home
      </Link>
    </div>
  );
}

export default NotFound;

import React from "react";
import { Link } from "react-router-dom";
import About from "../components/about";

const AboutPage = () => {
  document.title = "Market Mind";

  return (
    <div className="container mt-5">
      <About />
      <div className="text-center mt-4">
        <Link to="/" className="btn btn-primary btn-md">
          Back to Home
        </Link>
      </div>
    </div>
  );
};

export default AboutPage;

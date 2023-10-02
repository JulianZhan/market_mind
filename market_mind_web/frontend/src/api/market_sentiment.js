const API_BASE_URL = "http://localhost:8080/api/v1";

export const fetchAlphaVantageData = async (startDate, endDate) => {
  const response = await fetch(
    `${API_BASE_URL}/alphavantageagg/date-range?startDate=${startDate}&endDate=${endDate}`
  );
  return response.json();
};

export const fetchRedditData = async (startDate, endDate) => {
  const response = await fetch(
    `${API_BASE_URL}/redditagg/date-range?startDate=${startDate}&endDate=${endDate}`
  );
  return response.json();
};

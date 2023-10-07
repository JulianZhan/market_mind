import CONFIG from "../config";
import { adjustToLocalDate } from "../utils/dateUtils";
const API_BASE_URL = CONFIG.API_BASE_URL;

export const fetchAlphaVantageData = async (startDate, endDate) => {
  const response = await fetch(
    `${API_BASE_URL}/alphavantageagg/date-range?startDate=${startDate}&endDate=${endDate}`
  );
  const data = await response.json();

  return data.map((item) => ({
    ...item,
    dateRecorded: adjustToLocalDate(item.dateRecorded + "Z"),
  }));
};

export const fetchRedditData = async (startDate, endDate) => {
  const response = await fetch(
    `${API_BASE_URL}/redditagg/date-range?startDate=${startDate}&endDate=${endDate}`
  );
  const data = await response.json();

  return data.map((item) => ({
    ...item,
    dateRecorded: adjustToLocalDate(item.dateRecorded + "Z"),
  }));
};

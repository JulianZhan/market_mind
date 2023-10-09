import CONFIG from "../config";
import { adjustToLocalDate } from "../utils/dateUtils";
const API_BASE_URL = CONFIG.API_BASE_URL;

/**
 * Assign the fetch function to a constant to avoid repetition.
 * Use async/await to handle the promise returned by fetch and ensure
 * the code is executed sequentially.
 *  */
export const fetchAlphaVantageData = async (startDate, endDate) => {
  /**
   * This function fetches Alpha Vantage data from the server.
   * @Param {String} startDate - The start date of the data.
   * @Param {String} endDate - The end date of the data.
   * @Return {Array} - An array of alpha vantage data.
   */
  const response = await fetch(
    `${API_BASE_URL}/alphavantageagg/date-range?startDate=${startDate}&endDate=${endDate}`
  );
  const data = await response.json();

  /**
   * Use map to loop for each item in the data array, we convert the date to a local date.
   * ... is the spread operator. It spreads the properties of the item object
   * into the new object we are creating. We then overwrite the dateRecorded
   * property with the adjusted date.
   */
  return data.map((item) => ({
    ...item,
    // Append "Z" to the date string to indicate that it is UTC from server.
    dateRecorded: adjustToLocalDate(item.dateRecorded + "Z"),
  }));
};

export const fetchRedditData = async (startDate, endDate) => {
  /**
   * This function fetches Reddit data from the server.
   * @Param {String} startDate - The start date of the data.
   * @Param {String} endDate - The end date of the data.
   * @Return {Array} - An array of reddit data.
   */
  const response = await fetch(
    `${API_BASE_URL}/redditagg/date-range?startDate=${startDate}&endDate=${endDate}`
  );
  const data = await response.json();

  /**
   * Use map to loop for each item in the data array, we convert the date to a local date.
   * ... is the spread operator. It spreads the properties of the item object
   * into the new object we are creating. We then overwrite the dateRecorded
   * property with the adjusted date.
   */
  return data.map((item) => ({
    ...item,
    dateRecorded: adjustToLocalDate(item.dateRecorded + "Z"),
  }));
};

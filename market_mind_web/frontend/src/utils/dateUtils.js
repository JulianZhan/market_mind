export const adjustToLocalDate = (utcDate) => {
  /**
   * This function converts a UTC date string to a local date string.
   *
   * @Param {String} utcDate - A UTC date string.
   * @Return {String} - A local date string.
   */
  console.log("utcDate: ", utcDate);
  let localDate = new Date(utcDate);
  console.log("localDate: ", localDate);
  return localDate.toLocaleDateString();
};

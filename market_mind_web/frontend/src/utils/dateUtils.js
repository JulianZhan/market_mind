export const adjustToLocalDate = (utcDate) => {
  /**
   * This function converts a UTC date string to a local date string.
   *
   * @Param {String} utcDate - A UTC date string.
   * @Return {String} - A local date string.
   */
  let localDate = new Date(utcDate);
  return localDate.toLocaleDateString();
};

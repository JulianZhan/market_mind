export const adjustToLocalDate = (utcDate) => {
  console.log("utcDate: ", utcDate);
  let localDate = new Date(utcDate);
  console.log("localDate: ", localDate);
  return localDate.toLocaleDateString();
};

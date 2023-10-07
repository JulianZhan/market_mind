export const adjustToLocalDate = (utcDate) => {
  let localDate = new Date(utcDate);
  return localDate.toLocaleDateString();
};

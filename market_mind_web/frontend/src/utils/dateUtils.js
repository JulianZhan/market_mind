export const getUserTimezone = () => {
  return Intl.DateTimeFormat().resolvedOptions().timeZone;
};

export const adjustToLocalTime = (timestamp) => {
  const userTimezone = getUserTimezone();
  const date = new Date(timestamp);
  const userLocalDate = new Date(
    date.toLocaleString("en-US", { timeZone: userTimezone })
  );
  return userLocalDate.getTime();
};

export const adjustToLocalDate = (utcDate) => {
  let localDate = new Date(utcDate);
  return localDate.toLocaleDateString();
};

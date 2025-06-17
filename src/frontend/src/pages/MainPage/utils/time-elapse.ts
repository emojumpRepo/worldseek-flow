export const timeElapsed = (dateTimeString: string | undefined): string => {
  if (!dateTimeString) {
    return "";
  }

  const givenDate = new Date(dateTimeString);
  const now = new Date();

  let diffInMs = Math.abs(now.getTime() - givenDate.getTime());

  const minutes = Math.floor(diffInMs / (1000 * 60));
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  const months = Math.floor(days / 30); // Approximate
  const years = Math.floor(months / 12);

  if (years > 0) {
    return years === 1 ? `${years}年` : `${years}年`;
  } else if (months > 0) {
    return months === 1 ? `${months}月` : `${months}月`;
  } else if (days > 0) {
    return days === 1 ? `${days}天` : `${days}天`;
  } else if (hours > 0) {
    return hours === 1 ? `${hours}小时` : `${hours}小时`;
  } else if (minutes > 0) {
    return minutes === 1 ? `${minutes}分钟` : `${minutes}分钟`;
  } else {
    return "不到一分钟";
  }
};

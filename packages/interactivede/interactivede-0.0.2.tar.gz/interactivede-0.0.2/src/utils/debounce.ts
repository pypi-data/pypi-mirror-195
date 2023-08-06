export function debounce<Args extends readonly unknown[]>(
  func: (...args: Args) => void,
  wait = 300
) {
  let timeout: number | undefined;
  return (...args: Args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

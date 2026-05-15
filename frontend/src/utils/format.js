export function fmt(x, suffix = '') {
  return typeof x === 'number' ? `${x > 0 ? '+' : ''}${x.toFixed(2)}${suffix}` : x;
}

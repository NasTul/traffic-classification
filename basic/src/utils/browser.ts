export function parseQuery<T = any>(): T {
  const { search } = window.location;
  const r = /([^=&?#]+)=([^&#]*)/g;
  const matches = search.match(r);
  if (!matches || !matches.length) {
    return {} as any;
  }
  const query: any = {};
  matches.forEach(str => {
    const idx = str.indexOf('=');
    query[str.substr(0, idx)] = decodeURIComponent(str.substr(idx + 1));
  });
  return query;
}

/**
 * ApiClient – thin wrapper around the C-A-D-E backend REST API.
 * Used by the CLI so all commands talk to the same backend as the frontend.
 */

const DEFAULT_BASE = process.env.CADE_API_URL || 'http://localhost:8000';

export class ApiClient {
  constructor(baseUrl = DEFAULT_BASE) {
    this.baseUrl = baseUrl;
  }

  async _request(method, path, body) {
    const url = `${this.baseUrl}${path}`;
    const init = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body !== undefined) init.body = JSON.stringify(body);

    const res = await fetch(url, init);
    const text = await res.text();
    let data;
    try { data = JSON.parse(text); } catch { data = { raw: text }; }

    if (!res.ok) {
      const msg = data?.detail || data?.raw || res.statusText;
      throw new Error(`${method} ${path} → ${res.status}: ${msg}`);
    }
    return data;
  }

  get(path)        { return this._request('GET',    path); }
  post(path, body) { return this._request('POST',   path, body); }
  put(path, body)  { return this._request('PUT',    path, body); }
  del(path)        { return this._request('DELETE', path); }
}

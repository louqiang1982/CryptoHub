/**
 * API client layer — centralised HTTP client for all backend requests.
 *
 * Uses the native `fetch` API (available in Next.js 15 server/client
 * components) wrapped in a typed helper that handles:
 * - Base URL resolution (env-aware)
 * - Authorization header injection
 * - JSON serialisation / deserialisation
 * - Consistent error handling
 */

const GO_API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8080';
const PY_API_BASE = process.env.NEXT_PUBLIC_PY_API_URL ?? 'http://localhost:8000';

export class ApiError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    message?: string,
  ) {
    super(message ?? `API error ${status}: ${statusText}`);
    this.name = 'ApiError';
  }
}

type RequestOptions = RequestInit & {
  token?: string;
  base?: 'go' | 'python';
};

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { token, base = 'go', ...fetchOptions } = options;

  const baseUrl = base === 'python' ? PY_API_BASE : GO_API_BASE;
  const url = `${baseUrl}${path}`;

  const headers = new Headers(fetchOptions.headers);
  headers.set('Content-Type', 'application/json');
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(url, { ...fetchOptions, headers });

  if (!response.ok) {
    const body = await response.text().catch(() => '');
    throw new ApiError(response.status, response.statusText, body || undefined);
  }

  if (response.status === 204) {
    return undefined as unknown as T;
  }

  return response.json() as Promise<T>;
}

// ── Convenience helpers ───────────────────────────────────────────────────────

export function get<T>(path: string, opts?: RequestOptions): Promise<T> {
  return request<T>(path, { ...opts, method: 'GET' });
}

export function post<T>(path: string, body: unknown, opts?: RequestOptions): Promise<T> {
  return request<T>(path, {
    ...opts,
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export function put<T>(path: string, body: unknown, opts?: RequestOptions): Promise<T> {
  return request<T>(path, {
    ...opts,
    method: 'PUT',
    body: JSON.stringify(body),
  });
}

export function del<T>(path: string, opts?: RequestOptions): Promise<T> {
  return request<T>(path, { ...opts, method: 'DELETE' });
}

// ── Domain-specific API modules ───────────────────────────────────────────────

export const authApi = {
  login: (email: string, password: string) =>
    post<{ access_token: string; refresh_token: string }>('/api/auth/login', { email, password }),
  register: (email: string, password: string, name: string) =>
    post<{ access_token: string }>('/api/auth/register', { email, password, name }),
  refresh: (refreshToken: string) =>
    post<{ access_token: string }>('/api/auth/refresh', { refresh_token: refreshToken }),
  me: (token: string) =>
    get<{ id: string; email: string; name: string; role: string }>('/api/auth/me', { token }),
};

export const dashboardApi = {
  getSummary: (token: string) =>
    get<Record<string, unknown>>('/api/dashboard/summary', { token }),
};

export const marketApi = {
  getKlines: (symbol: string, interval: string, limit: number, token?: string) =>
    get<unknown[]>(`/api/market/kline?symbol=${symbol}&interval=${interval}&limit=${limit}`, { token }),
  getTicker: (symbol: string) =>
    get<Record<string, unknown>>(`/api/market/ticker?symbol=${symbol}`),
};

export const strategyApi = {
  list: (token: string) =>
    get<unknown[]>('/api/strategy', { token }),
  create: (data: Record<string, unknown>, token: string) =>
    post<{ id: string }>('/api/strategy', data, { token }),
  delete: (id: string, token: string) =>
    del(`/api/strategy/${id}`, { token }),
};

export const aiApi = {
  analyse: (symbol: string, timeframe: string, token: string) =>
    post<Record<string, unknown>>(
      '/api/ai/analyse',
      { symbol, timeframe },
      { token, base: 'python' },
    ),
  chat: (message: string, token: string) =>
    post<{ reply: string }>(
      '/api/ai/chat',
      { message },
      { token, base: 'python' },
    ),
};

export const polymarketApi = {
  getMarkets: (token?: string) =>
    get<unknown[]>('/api/polymarket/markets', { token, base: 'python' }),
  getMarket: (id: string, token?: string) =>
    get<Record<string, unknown>>(`/api/polymarket/markets/${id}`, { token, base: 'python' }),
};

export const credentialsApi = {
  list: (token: string) =>
    get<unknown[]>('/api/credentials', { token }),
  create: (data: Record<string, unknown>, token: string) =>
    post<{ id: string }>('/api/credentials', data, { token }),
  delete: (id: string, token: string) =>
    del(`/api/credentials/${id}`, { token }),
  verify: (id: string, token: string) =>
    post<{ verified: boolean }>(`/api/credentials/${id}/verify`, {}, { token }),
};

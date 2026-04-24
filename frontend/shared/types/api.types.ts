export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export type RequestOptions = {
  method?: HttpMethod;
  body?: unknown;
  accessToken?: string;
  headers?: HeadersInit;
  cache?: RequestCache;
  baseUrl?: string;
};

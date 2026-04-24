import type { RequestOptions } from "@/shared/types/api.types";

const baseApi = async <Type>(
  path: string,
  options: RequestOptions = {},
): Promise<Type | undefined> => {
  const {
    method = "GET",
    body,
    accessToken,
    headers,
    cache = "no-store",
    baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL,
  } = options;

  const response = await fetch(`${baseUrl}${path}`, {
    method,
    headers: {
      ...(body ? { "Content-Type": "application/json" } : {}),
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...headers,
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
    cache,
  });

  if (!response.ok) {
    const data = await response.json();
    throw new Error(data?.message || data?.detail || "Request failed");
  }

  return response.status === 204
    ? undefined
    : ((await response.json()) as Type);
};

export default baseApi;

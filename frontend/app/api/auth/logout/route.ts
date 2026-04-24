import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { env } from "@/shared/config/env";
import { AUTH_COOKIE_NAMES } from "@/shared/lib/auth/cookies";

export const POST = async () => {
  try {
    const cookieStore = await cookies();
    const accessToken = cookieStore.get(AUTH_COOKIE_NAMES.accessToken)?.value;
    const refreshToken = cookieStore.get(AUTH_COOKIE_NAMES.refreshToken)?.value;

    if (accessToken && refreshToken) {
      await fetch(`${env.apiBaseUrl}/api/auth/logout/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ refresh: refreshToken }),
        cache: "no-store",
      });
    }

    const response = NextResponse.json({ ok: true });

    response.cookies.delete(AUTH_COOKIE_NAMES.accessToken);
    response.cookies.delete(AUTH_COOKIE_NAMES.refreshToken);

    return response;
  } catch (error) {
    console.error("Logout route error:", error);

    const response = NextResponse.json(
      { message: "Internal server error during logout" },
      { status: 500 },
    );

    response.cookies.delete(AUTH_COOKIE_NAMES.accessToken);
    response.cookies.delete(AUTH_COOKIE_NAMES.refreshToken);

    return response;
  }
};

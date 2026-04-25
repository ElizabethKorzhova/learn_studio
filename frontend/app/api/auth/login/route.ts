import { NextResponse } from "next/server";
import { env } from "@/shared/config/env";
import {
  AUTH_COOKIE_NAMES,
  getAccessTokenCookieOptions,
  getRefreshTokenCookieOptions,
} from "@/shared/lib/auth/cookies";
import type {
  LoginDataType,
  TokenPair,
} from "@/features/auth/types/auth.types";
import { parseBackendResponse } from "@/app/api/auth/register/route";

export const POST = async (request: Request) => {
  try {
    const body = (await request.json()) as LoginDataType;

    const backendResponse = await fetch(`${env.apiBaseUrl}/api/auth/login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
      cache: "no-store",
    });

    const data = await parseBackendResponse(backendResponse);

    if (!backendResponse.ok) {
      return NextResponse.json(
        {
          message: data?.detail ?? "Login failed",
          errors: data,
        },
        { status: backendResponse.status },
      );
    }

    const { access, refresh } = data as TokenPair;

    if (!access || !refresh) {
      return NextResponse.json(
        {
          message: "Backend login response does not contain tokens",
        },
        { status: 500 },
      );
    }

    const response = NextResponse.json({ ok: true });

    response.cookies.set(
      AUTH_COOKIE_NAMES.accessToken,
      access,
      getAccessTokenCookieOptions(),
    );

    response.cookies.set(
      AUTH_COOKIE_NAMES.refreshToken,
      refresh,
      getRefreshTokenCookieOptions(),
    );

    return response;
  } catch (error) {
    console.error("Login route error:", error);

    return NextResponse.json(
      { message: "Internal server error during login" },
      { status: 500 },
    );
  }
};

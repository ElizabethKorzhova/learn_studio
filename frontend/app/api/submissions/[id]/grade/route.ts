import { NextResponse } from "next/server";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";
import { getSession } from "@/shared/lib/auth/getSession";

type RouteProps = {
  params: Promise<{ id: string }>;
};

export const PATCH = async (request: Request, { params }: RouteProps) => {
  const session = await getSession();

  if (!session) {
    return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;
  const body = await request.json();

  try {
    const result = await baseApi(routes.api.submissionGrade(id), {
      method: "PATCH",
      accessToken: session.accessToken,
      body,
    });

    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      {
        message:
          error instanceof Error
            ? error.message
            : "Failed to grade submissions",
      },
      { status: 400 },
    );
  }
};

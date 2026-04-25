import { NextResponse } from "next/server";
import baseApi from "@/shared/lib/api/baseApi";
import { getSession } from "@/shared/lib/auth/getSession";

export const POST = async (request: Request) => {
  const session = await getSession();

  if (!session) {
    return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
  }

  const url = new URL(request.url);
  const homeworkId = url.searchParams.get("homework_id");

  if (!homeworkId) {
    return NextResponse.json(
      { message: "homework_id is required" },
      { status: 400 },
    );
  }

  const body = await request.json();

  try {
    const submission = await baseApi(
      `/api/submissions/?homework_id=${homeworkId}`,
      {
        method: "POST",
        accessToken: session.accessToken,
        body,
      },
    );

    return NextResponse.json(submission, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      {
        message:
          error instanceof Error ? error.message : "Failed to submit solution",
      },
      { status: 400 },
    );
  }
};

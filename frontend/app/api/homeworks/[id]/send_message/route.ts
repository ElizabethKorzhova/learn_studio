import { NextResponse } from "next/server";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";
import { getSession } from "@/shared/lib/auth/getSession";

type RouteProps = {
  params: Promise<{ id: string }>;
};

export const POST = async (request: Request, { params }: RouteProps) => {
  const session = await getSession();

  if (!session) {
    return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;
  const body = await request.json();

  const url = new URL(request.url);
  const studentId = url.searchParams.get("student_id");

  const searchParams = new URLSearchParams();

  if (studentId) {
    searchParams.set("student_id", studentId);
  }

  const query = searchParams.toString();

  try {
    const message = await baseApi(
      routes.api.sendHomeworkMessage(id) + (query ? `?${query}` : ""),
      {
        method: "POST",
        accessToken: session.accessToken,
        body,
      },
    );

    return NextResponse.json(message, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      {
        message:
          error instanceof Error ? error.message : "Failed to send message",
      },
      { status: 400 },
    );
  }
};

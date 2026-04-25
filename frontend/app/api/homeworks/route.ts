import { NextResponse } from "next/server";
import { createHomework } from "@/features/homework/api/manageHomework";
import { getSession } from "@/shared/lib/auth/getSession";

export const POST = async (request: Request) => {
  const session = await getSession();

  if (!session) {
    return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
  }

  const url = new URL(request.url);
  const lessonId = url.searchParams.get("lesson_id");

  if (!lessonId) {
    return NextResponse.json(
      { message: "lesson_id is required" },
      { status: 400 },
    );
  }

  try {
    const body = await request.json();
    const homework = await createHomework(session.accessToken, lessonId, body);

    return NextResponse.json(homework, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      {
        message:
          error instanceof Error ? error.message : "Failed to create homework",
      },
      { status: 400 },
    );
  }
};

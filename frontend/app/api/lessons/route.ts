import { NextResponse } from "next/server";
import { createLesson } from "@/features/lesson/api/manageLesson";
import { getCourseById } from "@/features/course/api/getCourseById";
import { getCoursePermissions } from "@/shared/lib/auth/coursePermissions";
import { getSession } from "@/shared/lib/auth/getSession";

export const POST = async (request: Request) => {
  const session = await getSession();

  if (!session) {
    return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
  }

  const url = new URL(request.url);
  const courseId = url.searchParams.get("course_id");

  if (!courseId) {
    return NextResponse.json(
      { message: "course_id is required" },
      { status: 400 },
    );
  }

  try {
    const course = await getCourseById(session.accessToken, courseId);

    const permissions = getCoursePermissions({
      role: session.user.role,
      userId: session.user.id,
      course,
    });

    if (!permissions.canCreateLesson) {
      return NextResponse.json({ message: "Forbidden" }, { status: 403 });
    }

    const body = await request.json();
    const lesson = await createLesson(session.accessToken, courseId, body);

    return NextResponse.json(lesson, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { message: error instanceof Error ? error.message : "Request failed" },
      { status: 400 },
    );
  }
};

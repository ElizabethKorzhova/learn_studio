import { NextResponse } from "next/server";
import { createCourse } from "@/features/course/api/manageCourse";
import { canCreateCourse } from "@/shared/lib/auth/coursePermissions";
import { getSession } from "@/shared/lib/auth/getSession";

export const POST = async (request: Request) => {
  const session = await getSession();

  if (!session || !canCreateCourse(session.user.role)) {
    return NextResponse.json({ message: "Forbidden" }, { status: 403 });
  }

  try {
    const body = await request.json();
    const course = await createCourse(session.accessToken, body);

    return NextResponse.json(course, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { message: error instanceof Error ? error.message : "Request failed" },
      { status: 400 },
    );
  }
};

import { NextResponse } from "next/server";
import { deleteLesson, updateLesson } from "@/features/lesson/api/manageLesson";
import { getCourseById } from "@/features/course/api/getCourseById";
import { getCoursePermissions } from "@/shared/lib/auth/coursePermissions";
import { getSession } from "@/shared/lib/auth/getSession";

type LessonRouteProps = {
  params: Promise<{ id: string }>;
};

const getLessonAccess = async (
  request: Request,
  permission: "canEditLesson" | "canDeleteLesson",
) => {
  const session = await getSession();

  if (!session) {
    return {
      error: NextResponse.json({ message: "Unauthorized" }, { status: 401 }),
    };
  }

  const url = new URL(request.url);
  const courseId = url.searchParams.get("course_id");

  if (!courseId) {
    return {
      error: NextResponse.json(
        { message: "course_id is required" },
        { status: 400 },
      ),
    };
  }

  const course = await getCourseById(session.accessToken, courseId);

  const permissions = getCoursePermissions({
    role: session.user.role,
    userId: session.user.id,
    course,
  });

  if (!permissions[permission]) {
    return {
      error: NextResponse.json({ message: "Forbidden" }, { status: 403 }),
    };
  }

  return { session, courseId };
};

export const PATCH = async (request: Request, { params }: LessonRouteProps) => {
  const { id } = await params;

  try {
    const access = await getLessonAccess(request, "canEditLesson");

    if (access.error) return access.error;

    const body = await request.json();
    const lesson = await updateLesson(access.session.accessToken, id, body);

    return NextResponse.json(lesson, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      { message: error instanceof Error ? error.message : "Request failed" },
      { status: 400 },
    );
  }
};

export const DELETE = async (
  request: Request,
  { params }: LessonRouteProps,
) => {
  const { id } = await params;

  try {
    const access = await getLessonAccess(request, "canDeleteLesson");

    if (access.error) return access.error;

    await deleteLesson(access.session.accessToken, id);

    return new NextResponse(null, { status: 204 });
  } catch (error) {
    return NextResponse.json(
      { message: error instanceof Error ? error.message : "Request failed" },
      { status: 400 },
    );
  }
};

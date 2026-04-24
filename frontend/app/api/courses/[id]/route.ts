import { NextResponse } from "next/server";
import { deleteCourse, updateCourse } from "@/features/course/api/manageCourse";
import { getCourseById } from "@/features/course/api/getCourseById";
import { getCoursePermissions } from "@/shared/lib/auth/coursePermissions";
import { getSession } from "@/shared/lib/auth/getSession";

type CourseRouteProps = {
  params: Promise<{ id: string }>;
};

type CoursePermission = "canEditCourse" | "canDeleteCourse";

const getAuthorizedCourseContext = async (
  courseId: string,
  permission: CoursePermission,
) => {
  const session = await getSession();

  if (!session) {
    return {
      error: NextResponse.json({ message: "Unauthorized" }, { status: 401 }),
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

  return { session };
};

export const PATCH = async (request: Request, { params }: CourseRouteProps) => {
  const { id } = await params;

  try {
    const context = await getAuthorizedCourseContext(id, "canEditCourse");

    if (context.error) {
      return context.error;
    }

    const body = await request.json();
    const course = await updateCourse(context.session.accessToken, id, body);

    return NextResponse.json(course, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      { message: error instanceof Error ? error.message : "Request failed" },
      { status: 400 },
    );
  }
};

export const DELETE = async (
  _request: Request,
  { params }: CourseRouteProps,
) => {
  const { id } = await params;

  try {
    const context = await getAuthorizedCourseContext(id, "canDeleteCourse");

    if (context.error) {
      return context.error;
    }

    await deleteCourse(context.session.accessToken, id);

    return new NextResponse(null, { status: 204 });
  } catch (error) {
    return NextResponse.json(
      { message: error instanceof Error ? error.message : "Request failed" },
      { status: 400 },
    );
  }
};

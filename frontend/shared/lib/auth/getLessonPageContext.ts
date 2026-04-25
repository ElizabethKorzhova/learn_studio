import { notFound, redirect } from "next/navigation";

import { getCourseById } from "@/features/course/api/getCourseById";
import { getLessonById } from "@/features/lesson/api/getLessonById";
import { routes } from "@/shared/config/routes";
import { getCoursePermissions } from "@/shared/lib/auth/coursePermissions";
import { getSession } from "@/shared/lib/auth/getSession";

type GetLessonPageContextParams = {
  lessonIdParam: string;
  courseIdParam?: string;
};

export const getLessonPageContext = async ({
  lessonIdParam,
  courseIdParam,
}: GetLessonPageContextParams) => {
  const lessonId = Number(lessonIdParam);
  const courseId = Number(courseIdParam);

  if (Number.isNaN(lessonId) || Number.isNaN(courseId)) {
    notFound();
  }

  const session = await getSession();

  if (!session) {
    redirect(routes.courses);
  }

  const [lesson, course] = await Promise.all([
    getLessonById(session.accessToken, lessonId).catch(() => notFound()),
    getCourseById(session.accessToken, courseId).catch(() => notFound()),
  ]);

  const permissions = getCoursePermissions({
    role: session.user.role,
    userId: session.user.id,
    course,
  });

  return {
    lessonId,
    courseId,
    session,
    lesson,
    course,
    permissions,
  };
};

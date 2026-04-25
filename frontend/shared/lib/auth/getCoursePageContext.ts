import { notFound, redirect } from "next/navigation";
import { getCourseById } from "@/features/course/api/getCourseById";
import { routes } from "@/shared/config/routes";
import { getCoursePermissions } from "@/shared/lib/auth/coursePermissions";
import { getSession } from "@/shared/lib/auth/getSession";

export const getCoursePageContext = async (id: string) => {
  const courseId = Number(id);

  if (Number.isNaN(courseId)) {
    notFound();
  }

  const session = await getSession();

  if (!session) {
    redirect(routes.courses);
  }

  const course = await getCourseById(session.accessToken, courseId).catch(
    () => {
      notFound();
    },
  );

  const permissions = getCoursePermissions({
    role: session.user.role,
    userId: session.user.id,
    course,
  });

  return {
    courseId,
    session,
    course,
    permissions,
  };
};

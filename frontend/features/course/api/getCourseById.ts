import type { CourseDetail } from "@/features/course/types/course.types";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export const getCourseById = async (
  accessToken: string,
  courseId: number | string,
): Promise<CourseDetail> => {
  const course = await baseApi<CourseDetail>(
    routes.api.course(String(courseId)),
    {
      accessToken,
    },
  );

  if (!course) {
    throw new Error("Failed to fetch course detail");
  }

  return course;
};

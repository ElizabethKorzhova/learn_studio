import type { Course } from "@/features/course/types/course.types";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export const getMyCourses = async (accessToken: string): Promise<Course[]> => {
  return (
    (await baseApi<Course[]>(routes.api.myCourses, {
      accessToken,
    })) ?? []
  );
};

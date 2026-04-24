import type {
  Course,
  CoursePayload,
} from "@/features/course/types/course.types";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export const createCourse = async (
  accessToken: string,
  payload: CoursePayload,
): Promise<Course> => {
  const course = await baseApi<Course>(routes.api.courses, {
    method: "POST",
    accessToken,
    body: payload,
  });

  if (!course) {
    throw new Error("Failed to create course");
  }

  return course;
};

export const updateCourse = async (
  accessToken: string,
  courseId: string | number,
  payload: CoursePayload,
): Promise<Course> => {
  const course = await baseApi<Course>(routes.api.course(String(courseId)), {
    method: "PATCH",
    accessToken,
    body: payload,
  });

  if (!course) {
    throw new Error("Failed to update course");
  }

  return course;
};

export const deleteCourse = async (
  accessToken: string,
  courseId: string | number,
): Promise<void> => {
  await baseApi<void>(routes.api.course(String(courseId)), {
    method: "DELETE",
    accessToken,
  });
};

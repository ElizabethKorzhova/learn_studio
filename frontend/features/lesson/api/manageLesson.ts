import type {
  Lesson,
  LessonPayload,
} from "@/features/lesson/types/lesson.types";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export const createLesson = async (
  accessToken: string,
  courseId: number | string,
  payload: LessonPayload,
): Promise<Lesson> => {
  const lesson = await baseApi<Lesson>(routes.api.lessons(String(courseId)), {
    method: "POST",
    accessToken,
    body: payload,
  });

  if (!lesson) {
    throw new Error("Failed to create lesson");
  }

  return lesson;
};

export const updateLesson = async (
  accessToken: string,
  lessonId: number | string,
  payload: LessonPayload,
): Promise<Lesson> => {
  const lesson = await baseApi<Lesson>(routes.api.lesson(String(lessonId)), {
    method: "PATCH",
    accessToken,
    body: payload,
  });

  if (!lesson) {
    throw new Error("Failed to update lesson");
  }

  return lesson;
};

export const deleteLesson = async (
  accessToken: string,
  lessonId: number | string,
): Promise<void> => {
  await baseApi<void>(routes.api.lesson(String(lessonId)), {
    method: "DELETE",
    accessToken,
  });
};

import type { Lesson } from "@/features/lesson/types/lesson.types";
import baseApi from "@/shared/lib/api/baseApi";

export const getLessonById = async (
  accessToken: string,
  lessonId: number | string,
): Promise<Lesson> => {
  const lesson = await baseApi<Lesson>(`/api/lessons/${lessonId}/`, {
    accessToken,
  });

  if (!lesson) {
    throw new Error("Failed to fetch lesson");
  }

  return lesson;
};

import type { Homework } from "@/features/homework/types/homework.types";
import baseApi from "@/shared/lib/api/baseApi";

export const getHomeworksByLesson = async (
  accessToken: string,
  lessonId: number | string,
): Promise<Homework[]> => {
  return (
    (await baseApi<Homework[]>(`/api/homeworks/?lesson_id=${lessonId}`, {
      accessToken,
    })) ?? []
  );
};

import type { Homework } from "@/features/homework/types/homework.types";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export const getHomeworkById = async (
  accessToken: string,
  homeworkId: string | number,
): Promise<Homework> => {
  const homework = await baseApi<Homework>(routes.api.homework(homeworkId), {
    accessToken,
  });

  if (!homework) {
    throw new Error("Failed to fetch homework");
  }

  return homework;
};

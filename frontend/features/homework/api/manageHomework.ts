import type {
  Homework,
  HomeworkPayload,
} from "@/features/homework/types/homework.types";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export const createHomework = async (
  accessToken: string,
  lessonId: string | number,
  payload: HomeworkPayload,
): Promise<Homework> => {
  const homework = await baseApi<Homework>(routes.api.homeworks(lessonId), {
    method: "POST",
    accessToken,
    body: payload,
  });

  if (!homework) {
    throw new Error("Failed to create homework");
  }

  return homework;
};

export const updateHomework = async (
  accessToken: string,
  homeworkId: string | number,
  payload: HomeworkPayload,
): Promise<Homework> => {
  const homework = await baseApi<Homework>(routes.api.homework(homeworkId), {
    method: "PATCH",
    accessToken,
    body: payload,
  });

  if (!homework) {
    throw new Error("Failed to update homework");
  }

  return homework;
};

export const deleteHomework = async (
  accessToken: string,
  homeworkId: string | number,
): Promise<void> => {
  await baseApi<void>(routes.api.homework(homeworkId), {
    method: "DELETE",
    accessToken,
  });
};

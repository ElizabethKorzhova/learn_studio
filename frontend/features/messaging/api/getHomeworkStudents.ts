import type { HomeworkStudentListItem } from "@/features/messaging/types/message.types";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export const getHomeworkStudents = async (
  accessToken: string,
  homeworkId: string | number,
): Promise<HomeworkStudentListItem[]> => {
  return (
    (await baseApi<HomeworkStudentListItem[]>(
      routes.api.homeworkStudents(homeworkId),
      {
        accessToken,
      },
    )) ?? []
  );
};

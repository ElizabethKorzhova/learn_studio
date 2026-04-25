import type { Homework } from "@/features/homework/types/homework.types";
import type { HomeworkConversationDetail } from "@/features/messaging/types/message.types";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export const getHomeworkConversation = async (
  accessToken: string,
  homeworkId: string | number,
  studentId?: string | number,
): Promise<HomeworkConversationDetail<Homework>> => {
  const searchParams = new URLSearchParams();

  if (studentId !== undefined && studentId !== null) {
    searchParams.set("student_id", String(studentId));
  }

  const query = searchParams.toString();

  const conversation = await baseApi<HomeworkConversationDetail<Homework>>(
    `${routes.api.homeworkConversation(homeworkId)}${query ? `?${query}` : ""}`,
    {
      accessToken,
    },
  );

  if (!conversation) {
    throw new Error("Failed to fetch homework conversation");
  }

  return conversation;
};

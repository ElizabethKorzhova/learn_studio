import type {
  Message,
  MessageCreateDto,
} from "@/features/messaging/types/message.types";
import { routes } from "@/shared/config/routes";

export const sendHomeworkMessage = async (
  homeworkId: number,
  payload: MessageCreateDto,
  studentId?: number,
): Promise<Message> => {
  const searchParams = new URLSearchParams();

  if (studentId !== undefined && studentId !== null) {
    searchParams.set("student_id", String(studentId));
  }

  const query = searchParams.toString();

  const response = await fetch(
    `${routes.api.sendHomeworkMessage(homeworkId)}${query ? `?${query}` : ""}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    },
  );

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.message || data?.detail || "Failed to send message");
  }

  return data as Message;
};

import { env } from "@/shared/config/env";
import type { Submission } from "../types/submission.types";

export async function getSubmissionsByHomework(
  accessToken: string,
  homeworkId: number,
): Promise<Submission[]> {
  const response = await fetch(
    `${env.apiBaseUrl}/api/submissions/?homework_id=${homeworkId}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error("Failed to fetch submissions");
  }

  return response.json();
}

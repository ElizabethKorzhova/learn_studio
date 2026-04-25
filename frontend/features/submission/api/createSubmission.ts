import type { SubmissionCreateDto } from "../types/submission.types";

export async function createSubmission(
  homeworkId: number,
  payload: SubmissionCreateDto,
) {
  const response = await fetch(`/api/submissions?homework_id=${homeworkId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data?.message ?? "Failed to create submissions");
  }

  return data;
}

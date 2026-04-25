import { routes } from "@/shared/config/routes";

export type GradeSubmissionPayload = {
  score: number;
};

export const gradeSubmission = async (
  submissionId: number,
  payload: GradeSubmissionPayload,
) => {
  const response = await fetch(routes.api.submissionGrade(submissionId), {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      data?.message || data?.detail || "Failed to grade submissions",
    );
  }

  return data;
};

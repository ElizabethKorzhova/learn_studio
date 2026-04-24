import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";
import {
  Enrollment,
  CreateEnrollmentPayload,
} from "@/features/course/types/course.types";

export const createEnrollment = async (
  accessToken: string,
  payload: CreateEnrollmentPayload,
): Promise<Enrollment> => {
  const enrollment = await baseApi<Enrollment>(routes.api.enrollments, {
    method: "POST",
    accessToken,
    body: payload,
  });

  if (!enrollment) {
    throw new Error("Failed to enroll");
  }

  return enrollment;
};

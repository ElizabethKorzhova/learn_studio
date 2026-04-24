import type { CourseDetail } from "@/features/course/types/course.types";
import { isInstructorRole, isStudentRole } from "@/shared/lib/auth/roles";

export const canCreateCourse = (role: string | null | undefined): boolean =>
  isInstructorRole(role);

export const getCoursePermissions = ({
  role,
  userId,
  course,
}: {
  role: string | null | undefined;
  userId: number | null | undefined;
  course: CourseDetail;
}) => {
  const isOwner =
    isInstructorRole(role) &&
    userId != null &&
    course.instructor?.id != null &&
    userId === course.instructor.id;

  const isEnrolled =
    course.is_enrolled === true || course.is_enrolled === "true";

  return {
    canCreateCourse: canCreateCourse(role),

    canEditCourse: isOwner,
    canDeleteCourse: isOwner,

    canOpenLessons: isOwner || isEnrolled,

    canCreateLesson: isOwner,
    canEditLesson: isOwner,
    canDeleteLesson: isOwner,

    canCreateHomework: isOwner,
    canEditHomework: isOwner,
    canDeleteHomework: isOwner,

    canMessageStudent: isOwner,
    canGradeSubmission: isOwner,

    canEnroll: isStudentRole(role) && !isEnrolled,

    isCourseOwner: isOwner,
    isEnrolled,
  };
};

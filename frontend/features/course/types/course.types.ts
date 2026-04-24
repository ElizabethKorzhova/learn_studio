import { getCoursePermissions } from "@/shared/lib/auth/coursePermissions";

export interface CourseInstructor {
  id: number;
  username?: string;
  email?: string;
  first_name: string;
  last_name: string;
}

export interface Course {
  id: number;
  title: string;
  description: string;
  price: string | null;
  start_at: string;
  duration: number;
  is_enrolled: boolean | string;
  instructor: CourseInstructor;
}

export interface LessonShort {
  id: number;
  title: string;
  order_index: number;
}

export interface CourseDetail extends Course {
  lessons: LessonShort[];
}

export interface CoursePayload {
  title: string;
  description: string;
  start_at: string;
  duration: number;
  price: string | null;
}

export type CreateEnrollmentPayload = {
  course: number;
};

export type Enrollment = {
  id: number;
  course: number;
  student: number;
};

export interface CourseCardProps {
  course: Course;
}

export type CourseDetailsProps = {
  course: CourseDetail;
  courseId: number;
  permissions: ReturnType<typeof getCoursePermissions>;
};

export type CourseFormMode = "create" | "edit";

export type CourseFormProps = {
  mode: CourseFormMode;
  courseId?: number;
  initialValues?: Course | CoursePayload;
  submitLabel: string;
  title: string;
};

export type CourseFormValues = {
  title: string;
  description: string;
  start_at: string;
  duration: number;
  price: string;
};

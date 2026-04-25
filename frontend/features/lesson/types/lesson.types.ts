export interface Lesson {
  id: number;
  title: string;
  content: string;
  order_index: number;
  images: string | null;
  course: number;
}

export interface LessonPayload {
  title: string;
  content: string;
  order_index: number;
  images: string | null;
}

export type LessonFormMode = "create" | "edit";

export type LessonFormProps = {
  mode: LessonFormMode;
  courseId: number;
  lessonId?: number;
  initialValues?: Lesson;
  submitLabel: string;
  title: string;
};

export type LessonFormValues = {
  title: string;
  content: string;
  order_index: number;
  images: string;
};

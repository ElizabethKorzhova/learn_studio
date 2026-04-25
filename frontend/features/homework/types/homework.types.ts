import type { HomeworkStudentListItem } from "@/features/messaging/types/message.types";

export interface UserShort {
  id: number;
  first_name: string;
  last_name: string;
}

export interface Homework {
  id: number;
  title: string;
  task: string;
  deadline: string;
  deadline_date: string;
  complexity: number;
  created_by: UserShort;
}

export interface HomeworkPayload {
  title: string;
  task: string;
  deadline: string;
  deadline_date: string;
  complexity: number;
}

type HomeworkFormMode = "create" | "edit";

export type HomeworkFormProps = {
  mode: HomeworkFormMode;
  lessonId?: number;
  homeworkId?: number;
  initialValues?: Homework;
  title: string;
  submitLabel: string;
};

export type HomeworkFormValues = {
  title: string;
  task: string;
  deadline: string;
  complexity: number;
};

export type HomeworkInfoCardProps = {
  homework: Homework;
  canManageHomework: boolean;
};

export type HomeworkStudentSelectorProps = {
  homeworkId: number;
  students: HomeworkStudentListItem[];
  selectedStudentId?: number;
};

export type HomeworkSubmissionsProps = {
  submissions: any[];
  canGrade: boolean;
};

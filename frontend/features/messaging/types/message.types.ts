export interface UserShort {
  id: number;
  first_name: string;
  last_name: string;
}

export interface Message {
  id: number;
  conversation: number | null;
  sender: UserShort;
  message_text: string;
  created_at: string;
}

export interface MessageCreateDto {
  message_text: string;
}

export interface HomeworkConversation {
  id: number;
  homework: number;
  student: UserShort;
  instructor: UserShort;
  created_at: string;
  updated_at: string;
}

export interface HomeworkConversationDetail<THomework = unknown> {
  homework: THomework;
  conversation: HomeworkConversation;
  messages: Message[];
}

export interface HomeworkStudentListItem {
  student: UserShort;
}

export type ChatSocketPayload = {
  type: string;
  message: Message;
};

export type HomeworkChatProps = {
  initialData: HomeworkConversationDetail | null;
  homeworkId: number;
  studentId?: number;
  accessToken: string;
};

export type MessageFormProps = {
  homeworkId: number;
  studentId?: number;
  onSuccess?: (message: Message) => void;
};

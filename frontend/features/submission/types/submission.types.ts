export interface UserShort {
  id: number;
  first_name: string;
  last_name: string;
}

export interface Submission {
  id: number;
  user: UserShort;
  files: string | null;
  url: string | null;
  submitted_at: string;
  score: number | null;
  homework: number;
}

export interface SubmissionCreateDto {
  url?: string;
}

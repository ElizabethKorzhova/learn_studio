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

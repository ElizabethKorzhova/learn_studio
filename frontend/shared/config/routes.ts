export const routes = {
  home: "/",
  login: "/login",
  register: "/register",
  profile: "/profile",
  dashboard: "/dashboard",

  courses: "/courses",
  myCourses: "/my-courses",
  newCourse: "/courses/new",
  course: (id: string | number) => `/courses/${id}`,
  editCourse: (id: string | number) => `/courses/${id}/edit`,

  newLesson: (id: string | number) => `/courses/${id}/lessons/new`,
  lesson: (id: string | number) => `/lessons/${id}`,
  editLesson: (id: string | number) => `/lessons/${id}/edit`,

  newHomework: (lessonId: string | number) =>
    `/lessons/${lessonId}/homeworks/new`,
  homework: (id: string | number) => `/homeworks/${id}`,
  editHomework: (id: string | number) => `/homeworks/${id}/edit`,

  api: {
    login: "/api/auth/login/",
    logout: "/api/auth/logout/",
    register: "/api/auth/register/",
    tokenRefresh: "/api/auth/token/refresh/",
    profile: "/api/users/me/",

    courses: "/api/courses/",
    myCourses: "/api/courses/my/",
    course: (id: string | number) => `/api/courses/${id}/`,

    enrollments: "/api/enrollments/",

    lessons: (courseId: string | number) =>
      `/api/lessons/?course_id=${courseId}`,
    lesson: (id: string | number) => `/api/lessons/${id}/`,

    homeworks: (lessonId: string | number) =>
      `/api/homeworks/?lesson_id=${lessonId}`,
    homework: (id: string | number) => `/api/homeworks/${id}/`,

    homeworkConversation: (id: string | number) =>
      `/api/homeworks/${id}/conversation/`,
    homeworkStudents: (id: string | number) => `/api/homeworks/${id}/students/`,
    sendHomeworkMessage: (id: string | number) =>
      `/api/homeworks/${id}/send_message/`,

    submissions: (homeworkId: string | number) =>
      `/api/submissions/?homework_id=${homeworkId}`,
    submissionGrade: (id: string | number) => `/api/submissions/${id}/grade/`,
  },
} as const;

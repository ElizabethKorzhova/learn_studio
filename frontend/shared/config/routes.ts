export const routes = {
  home: "/",
  login: "/login",
  register: "/register",
  profile: "/profile",
  dashboard: "/dashboard",
  courses: "/courses",
  myCourses: "/my-courses",
  newCourse: "/courses/new",
  course: (id: string) => `/courses/${id}`,
  editCourse: (id: string) => `/courses/${id}/edit`,

  newLesson: (courseId: string) => `/courses/${courseId}/lessons/new`,
  lesson: (courseId: string, lessonId: string) =>
    `/courses/${courseId}/lessons/${lessonId}`,
  editLesson: (courseId: string, lessonId: string) =>
    `/courses/${courseId}/lessons/${lessonId}/edit`,
  api: {
    login: "/api/auth/login/",
    logout: "/api/auth/logout/",
    register: "/api/auth/register/",
    tokenRefresh: "/api/auth/token/refresh/",
    profile: "/api/users/me/",
    courses: "/api/courses/",
    myCourses: "/api/courses/my/",
    course: (id: string) => `/api/courses/${id}/`,
    enrollments: "/api/enrollments/",
  },
} as const;

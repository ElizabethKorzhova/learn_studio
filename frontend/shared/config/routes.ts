export const routes = {
  home: "/",
  login: "/login",
  register: "/register",
  dashboard: "/dashboard",
  courses: "/courses",
  course: (id: string) => `/courses/${id}`,
  lesson: (courseId: string, lessonId: string) =>
    `/courses/${courseId}/lessons/${lessonId}`,
  api: {
    login: "/api/auth/login/",
    logout: "/api/auth/logout/",
    register: "/api/auth/register/",
    tokenRefresh: "/api/auth/token/refresh/",
  },
} as const;

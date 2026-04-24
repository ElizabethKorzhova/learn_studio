const INSTRUCTOR_ROLES = new Set(["instructor", "admin"]);

export const normalizeRole = (role: string | null | undefined): string =>
  String(role ?? "")
    .trim()
    .toLowerCase();

export const isInstructorRole = (role: string | null | undefined): boolean =>
  INSTRUCTOR_ROLES.has(normalizeRole(role));

export const isStudentRole = (role: string | null | undefined): boolean =>
  normalizeRole(role) === "student";

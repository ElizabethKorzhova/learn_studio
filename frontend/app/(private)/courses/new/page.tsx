import { redirect } from "next/navigation";
import CourseForm from "@/features/course/components/CourseForm";
import { routes } from "@/shared/config/routes";
import { getSession } from "@/shared/lib/auth/getSession";
import { canCreateCourse } from "@/shared/lib/auth/coursePermissions";

const NewCoursePage = async () => {
  const session = await getSession();

  if (!session || !canCreateCourse(session.user.role)) {
    redirect(routes.myCourses);
  }

  return (
    <CourseForm
      mode="create"
      submitLabel="Create course"
      title="Create new course"
    />
  );
};

export default NewCoursePage;

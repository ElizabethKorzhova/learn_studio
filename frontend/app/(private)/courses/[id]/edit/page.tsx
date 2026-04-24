import { notFound, redirect } from "next/navigation";
import { getCourseById } from "@/features/course/api/getCourseById";
import CourseForm from "@/features/course/components/CourseForm";
import { routes } from "@/shared/config/routes";
import { getCoursePermissions } from "@/shared/lib/auth/coursePermissions";
import { getSession } from "@/shared/lib/auth/getSession";

interface EditCoursePageProps {
  params: Promise<{ id: string }>;
}

const EditCoursePage = async ({ params }: EditCoursePageProps) => {
  const { id } = await params;
  const courseId = Number(id);

  if (Number.isNaN(courseId)) {
    notFound();
  }

  const session = await getSession();

  if (!session) {
    redirect(routes.courses);
  }

  const course = await getCourseById(session.accessToken, courseId).catch(
    () => {
      notFound();
    },
  );

  const permissions = getCoursePermissions({
    role: session.user.role,
    userId: session.user.id,
    course,
  });

  if (!permissions.canEditCourse) {
    redirect(routes.course(String(courseId)));
  }

  return (
    <CourseForm
      mode="edit"
      courseId={courseId}
      initialValues={course}
      submitLabel="Save changes"
      title="Edit course"
    />
  );
};

export default EditCoursePage;

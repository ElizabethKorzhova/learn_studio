import { redirect } from "next/navigation";
import CourseForm from "@/features/course/components/CourseForm";
import { routes } from "@/shared/config/routes";
import { getCoursePageContext } from "@/shared/lib/auth/getCoursePageContext";

interface EditCoursePageProps {
  params: Promise<{ id: string }>;
}

const EditCoursePage = async ({ params }: EditCoursePageProps) => {
  const { id } = await params;

  const { courseId, course, permissions } = await getCoursePageContext(id);

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

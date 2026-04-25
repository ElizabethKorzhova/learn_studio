import { redirect } from "next/navigation";
import LessonForm from "@/features/lesson/components/LessonForm";
import { routes } from "@/shared/config/routes";
import { getCoursePageContext } from "@/shared/lib/auth/getCoursePageContext";

type NewLessonPageProps = {
  params: Promise<{ id: string }>;
};

const NewLessonPage = async ({ params }: NewLessonPageProps) => {
  const { id } = await params;

  const { courseId, permissions } = await getCoursePageContext(id);

  if (!permissions.canCreateLesson) {
    redirect(routes.course(String(courseId)));
  }
  return (
    <LessonForm
      mode="create"
      courseId={courseId}
      submitLabel="Create lesson"
      title="Create new lesson"
    />
  );
};

export default NewLessonPage;

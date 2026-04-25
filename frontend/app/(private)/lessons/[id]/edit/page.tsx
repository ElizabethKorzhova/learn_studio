import { redirect } from "next/navigation";
import LessonForm from "@/features/lesson/components/LessonForm";
import { routes } from "@/shared/config/routes";
import { getLessonPageContext } from "@/shared/lib/auth/getLessonPageContext";

type EditLessonPageProps = {
  params: Promise<{ id: string }>;
  searchParams?: Promise<{ course_id?: string }>;
};

const EditLessonPage = async ({
  params,
  searchParams,
}: EditLessonPageProps) => {
  const { id } = await params;
  const resolvedSearchParams = searchParams ? await searchParams : {};

  const { lessonId, courseId, lesson, permissions } =
    await getLessonPageContext({
      lessonIdParam: id,
      courseIdParam: resolvedSearchParams.course_id,
    });

  if (!permissions.canEditLesson) {
    redirect(routes.course(String(courseId)));
  }

  return (
    <LessonForm
      mode="edit"
      courseId={courseId}
      lessonId={lessonId}
      initialValues={lesson}
      submitLabel="Save changes"
      title="Edit lesson"
    />
  );
};

export default EditLessonPage;

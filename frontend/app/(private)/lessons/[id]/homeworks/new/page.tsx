import { redirect } from "next/navigation";
import HomeworkForm from "@/features/homework/components/HomeworkForm";
import { routes } from "@/shared/config/routes";
import { getLessonPageContext } from "@/shared/lib/auth/getLessonPageContext";

type NewHomeworkPageProps = {
  params: Promise<{ id: string }>;
  searchParams?: Promise<{ course_id?: string }>;
};

const NewHomeworkPage = async ({
  params,
  searchParams,
}: NewHomeworkPageProps) => {
  const { id } = await params;
  const resolvedSearchParams = searchParams ? await searchParams : {};

  const { lessonId, permissions } = await getLessonPageContext({
    lessonIdParam: id,
    courseIdParam: resolvedSearchParams.course_id,
  });

  if (!permissions.canCreateHomework) {
    redirect(routes.lesson(lessonId));
  }

  return (
    <HomeworkForm
      mode="create"
      lessonId={lessonId}
      title="Create homework"
      submitLabel="Create homework"
    />
  );
};

export default NewHomeworkPage;

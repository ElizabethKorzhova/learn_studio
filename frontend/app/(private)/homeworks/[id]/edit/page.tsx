import { notFound, redirect } from "next/navigation";
import { getHomeworkById } from "@/features/homework/api/getHomeworkById";
import HomeworkForm from "@/features/homework/components/HomeworkForm";
import { routes } from "@/shared/config/routes";
import { getSession } from "@/shared/lib/auth/getSession";
import { isInstructorRole } from "@/shared/lib/auth/roles";

type EditHomeworkPageProps = {
  params: Promise<{ id: string }>;
};

const EditHomeworkPage = async ({ params }: EditHomeworkPageProps) => {
  const { id } = await params;
  const homeworkId = Number(id);

  if (Number.isNaN(homeworkId)) {
    notFound();
  }

  const session = await getSession();

  if (!session || !isInstructorRole(session.user.role)) {
    redirect(routes.homework(homeworkId));
  }

  const homework = await getHomeworkById(session.accessToken, homeworkId).catch(
    () => notFound(),
  );

  return (
    <HomeworkForm
      mode="edit"
      homeworkId={homeworkId}
      initialValues={homework}
      title="Edit homework"
      submitLabel="Save changes"
    />
  );
};

export default EditHomeworkPage;

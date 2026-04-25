import { notFound, redirect } from "next/navigation";
import { getHomeworkById } from "@/features/homework/api/getHomeworkById";
import HomeworkInfoCard from "@/features/homework/components/HomeworkInfoCard";
import HomeworkStudentSelector from "@/features/homework/components/HomeworkStudentSelector";
import HomeworkSubmissions from "@/features/homework/components/HomeworkSubmissions";
import { getHomeworkConversation } from "@/features/messaging/api/getHomeworkConversation";
import { getHomeworkStudents } from "@/features/messaging/api/getHomeworkStudents";
import { HomeworkChat } from "@/features/messaging/components/HomeworkChat";
import { SubmissionForm } from "@/features/submission/components/SubmissionForm";
import { getSubmissionsByHomework } from "@/features/submission/api/getSubmissionsByHomework";
import { routes } from "@/shared/config/routes";
import { getSession } from "@/shared/lib/auth/getSession";
import { isInstructorRole } from "@/shared/lib/auth/roles";
import BackButton from "@/shared/components/BackButton";

type HomeworkPageProps = {
  params: Promise<{ id: string }>;
  searchParams?: Promise<{ student_id?: string }>;
};

const HomeworkPage = async ({ params, searchParams }: HomeworkPageProps) => {
  const { id } = await params;
  const resolvedSearchParams = searchParams ? await searchParams : {};

  const homeworkId = Number(id);

  if (Number.isNaN(homeworkId)) {
    notFound();
  }

  const session = await getSession();

  if (!session) {
    redirect(routes.courses);
  }

  const isInstructor = isInstructorRole(session.user.role);

  const selectedStudentId = resolvedSearchParams.student_id
    ? Number(resolvedSearchParams.student_id)
    : undefined;

  if (selectedStudentId !== undefined && Number.isNaN(selectedStudentId)) {
    notFound();
  }

  const homework = await getHomeworkById(session.accessToken, homeworkId).catch(
    () => notFound(),
  );

  const students = isInstructor
    ? await getHomeworkStudents(session.accessToken, homeworkId).catch(() => [])
    : [];

  const effectiveStudentId =
    isInstructor && selectedStudentId !== undefined
      ? students.find((item) => item.student.id === selectedStudentId)?.student
          .id
      : undefined;

  const submissions = await getSubmissionsByHomework(
    session.accessToken,
    homeworkId,
  ).catch(() => []);

  const displaySubmissions =
    isInstructor && effectiveStudentId !== undefined
      ? submissions.filter(
          (submission) => submission.user.id === effectiveStudentId,
        )
      : !isInstructor
        ? submissions
        : [];

  const shouldLoadConversation =
    !isInstructor || effectiveStudentId !== undefined;

  const conversation = shouldLoadConversation
    ? await getHomeworkConversation(
        session.accessToken,
        homeworkId,
        isInstructor ? effectiveStudentId : undefined,
      ).catch(() => null)
    : null;

  return (
    <section className="mx-auto w-full max-w-7xl space-y-6 px-4 py-8">
      <BackButton />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,1fr)_420px] lg:items-start">
        <div className="min-w-0 space-y-6">
          <HomeworkInfoCard
            homework={homework}
            canManageHomework={isInstructor}
          />

          {isInstructor && (
            <HomeworkStudentSelector
              homeworkId={homework.id}
              students={students}
              selectedStudentId={effectiveStudentId}
            />
          )}

          {isInstructor && effectiveStudentId === undefined ? (
            <div className="border-primary-light text-primary-grey rounded-4xl border-2 border-dashed p-10 text-center text-sm">
              Select a student to view submissions and conversation.
            </div>
          ) : (
            <section className="space-y-4">
              <h2 className="text-primary-dark px-2 text-xl font-bold">
                Submissions
              </h2>

              <HomeworkSubmissions
                submissions={displaySubmissions}
                canGrade={isInstructor}
              />
            </section>
          )}
        </div>

        <aside className="min-w-0 space-y-6 lg:sticky lg:top-8">
          {!isInstructor && (
            <section className="ring-primary-light rounded-4xl bg-white p-6 shadow-sm ring-1">
              <h2 className="text-primary-dark text-lg font-bold">
                Submit solution
              </h2>

              <p className="text-primary-grey mt-2 text-xs leading-relaxed">
                Provide a link to your solution.
              </p>

              <div className="mt-5">
                <SubmissionForm homeworkId={homework.id} />
              </div>
            </section>
          )}

          {(!isInstructor || effectiveStudentId !== undefined) && (
            <section className="ring-primary-light rounded-4xl bg-white p-6 shadow-sm ring-1">
              <h2 className="text-primary-dark mb-6 text-xl font-bold">
                Conversation
              </h2>

              {conversation ? (
                <HomeworkChat
                  initialData={conversation}
                  homeworkId={homeworkId}
                  studentId={isInstructor ? effectiveStudentId : undefined}
                  accessToken={session.accessToken}
                />
              ) : (
                <div className="border-primary-light text-primary-grey rounded-3xl border-2 border-dashed p-10 text-center text-sm">
                  No conversation yet.
                </div>
              )}
            </section>
          )}
        </aside>
      </div>
    </section>
  );
};

export default HomeworkPage;

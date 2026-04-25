import { redirect } from "next/navigation";
import ActionButton from "@/shared/components/ActionButton";
import BackButton from "@/shared/components/BackButton";
import Title from "@/shared/components/Title";
import { routes } from "@/shared/config/routes";
import DeleteLessonButton from "@/features/lesson/components/DeleteLessonButton";
import Link from "next/link";
import { getLessonPageContext } from "@/shared/lib/auth/getLessonPageContext";
import { getHomeworksByLesson } from "@/features/homework/api/getHomeworkByLesson";

type LessonPageProps = {
  params: Promise<{ id: string }>;
  searchParams?: Promise<{ course_id?: string }>;
};

const LessonPage = async ({ params, searchParams }: LessonPageProps) => {
  const { id } = await params;
  const resolvedSearchParams = searchParams ? await searchParams : {};

  const { lessonId, courseId, lesson, permissions, session } =
    await getLessonPageContext({
      lessonIdParam: id,
      courseIdParam: resolvedSearchParams.course_id,
    });

  if (!permissions.canOpenLessons) {
    redirect(routes.course(String(courseId)));
  }

  const homeworks = await getHomeworksByLesson(
    session.accessToken,
    lessonId,
  ).catch(() => []);
  return (
    <section className="mx-auto w-full max-w-5xl space-y-8">
      <BackButton />

      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div className="space-y-2">
          <Title title="Lesson" />
        </div>
      </div>

      <article className="ring-primary-light rounded-3xl bg-white p-8 shadow-sm ring-1">
        <div className="flex items-center gap-3 pb-7">
          <span className="bg-primary-light text-primary-accent flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl text-sm font-black">
            {lesson.order_index}
          </span>

          <h5 className="text-primary-dark text-3xl font-bold tracking-tight">
            {lesson.title}
          </h5>
        </div>
        <p className="text-primary-grey/40 mb-6 text-xs font-black tracking-widest uppercase">
          Lesson Content
        </p>

        <div className="text-primary-dark/80 pb-7 text-base leading-relaxed whitespace-pre-wrap">
          {lesson.content}
        </div>

        {permissions.canEditLesson && (
          <div className="border-primary-light flex flex-wrap justify-end gap-3 border-t pt-6">
            <ActionButton
              label="Edit lesson"
              href={`${routes.editLesson(String(lesson.id))}?course_id=${courseId}`}
              variant="outline"
            />

            <DeleteLessonButton lessonId={lesson.id} courseId={courseId} />
          </div>
        )}
      </article>

      <section className="space-y-6">
        <div className="flex w-full items-center justify-between">
          <h5 className="text-primary-dark text-xl font-bold whitespace-nowrap">
            Homework
          </h5>

          {permissions.canCreateHomework && (
            <ActionButton
              label="Add homework"
              href={routes.newHomework(lesson.id)}
            />
          )}
        </div>

        {homeworks.length === 0 ? (
          <div className="bg-primary-light/30 rounded-3xl p-10 text-center">
            <p className="text-primary-grey text-sm">No homework assigned</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {homeworks.map((hw) => (
              <Link
                key={hw.id}
                href={routes.homework(hw.id)}
                className="ring-primary-light block rounded-3xl bg-white p-6 shadow-sm ring-1 transition hover:shadow-md"
              >
                <h4 className="text-primary-dark font-bold">{hw.title}</h4>
              </Link>
            ))}
          </div>
        )}
      </section>
    </section>
  );
};

export default LessonPage;

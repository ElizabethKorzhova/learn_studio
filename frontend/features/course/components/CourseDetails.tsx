import Link from "next/link";
import { routes } from "@/shared/config/routes";
import ActionButton from "@/shared/components/ActionButton";
import EnrollButton from "./EnrollButton";
import DeleteCourseButton from "./DeleteCourseButton";
import BackButton from "@/shared/components/BackButton";
import Title from "@/shared/components/Title";
import { formatDate } from "@/shared/lib/date/formatDate";
import { CourseDetailsProps } from "@/features/course/types/course.types";
import DetailItem from "@/shared/components/DetailItem";

const CourseDetails = ({
  course,
  courseId,
  permissions,
}: CourseDetailsProps) => (
  <section className="mx-auto w-full max-w-7xl space-y-6">
    <BackButton />
    <Title title="Course details" />
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-[350px_1fr]">
      <div className="ring-primary-light h-fit space-y-6 rounded-3xl bg-white p-6 shadow-sm ring-1">
        <div>
          <h4 className="text-primary-dark text-2xl font-bold">
            {course.title}
          </h4>

          <p className="text-primary-grey mt-3 text-sm leading-relaxed">
            {course.description}
          </p>
        </div>

        <div className="border-primary-light space-y-4 border-t pt-6">
          <DetailItem label="Duration" value={course.duration} />
          <DetailItem label="Start Date" value={formatDate(course.start_at)} />
          <DetailItem label="Price" value={course.price ?? "Free"} />
        </div>
        <div className="flex w-full flex-col gap-2">
          {permissions.canEditCourse && (
            <ActionButton
              label="Edit course"
              href={routes.editCourse(String(courseId))}
              variant="outline"
            />
          )}

          {permissions.canDeleteCourse && (
            <DeleteCourseButton courseId={courseId} />
          )}

          {permissions.canEnroll && <EnrollButton courseId={courseId} />}
        </div>
      </div>
      <div className="space-y-6">
        <div className="ring-primary-light flex items-center justify-between rounded-3xl bg-white p-6 shadow-sm ring-1">
          <div>
            <h2 className="text-primary-dark text-lg font-bold">Lessons</h2>
            <p className="text-primary-grey text-sm">
              {course.lessons.length} modules available
            </p>
          </div>

          {permissions.canCreateLesson && (
            <ActionButton
              label="Add lesson"
              href={routes.newLesson(String(courseId))}
            />
          )}
        </div>

        <div className="space-y-4">
          {course.lessons.map((lesson) => (
            <div
              key={lesson.id}
              className="ring-primary-light flex items-center justify-between rounded-3xl bg-white p-5 shadow-sm ring-1"
            >
              <div className="flex items-center gap-4">
                <div className="bg-primary-light text-primary-accent flex h-10 w-10 items-center justify-center rounded-2xl text-sm font-bold">
                  {lesson.order_index}
                </div>

                {permissions.canOpenLessons ? (
                  <Link
                    href={routes.lesson(String(courseId), String(lesson.id))}
                    className="text-primary-dark hover:text-primary-accent font-bold"
                  >
                    {lesson.title}
                  </Link>
                ) : (
                  <span className="text-primary-dark font-bold">
                    {lesson.title}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </section>
);

export default CourseDetails;

import { notFound } from "next/navigation";
import { getCourseById } from "@/features/course/api/getCourseById";
import CourseDetails from "@/features/course/components/CourseDetails";
import { getCoursePermissions } from "@/shared/lib/auth/coursePermissions";
import { getSession } from "@/shared/lib/auth/getSession";

interface CourseDetailPageProps {
  params: Promise<{ id: string }>;
}

const CourseDetailPage = async ({ params }: CourseDetailPageProps) => {
  const { id } = await params;
  const courseId = Number(id);

  if (Number.isNaN(courseId)) {
    notFound();
  }

  const session = await getSession();

  if (!session) {
    notFound();
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

  return (
    <CourseDetails
      course={course}
      courseId={courseId}
      permissions={permissions}
    />
  );
};

export default CourseDetailPage;

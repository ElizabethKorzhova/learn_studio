import { getSession } from "@/shared/lib/auth/getSession";
import { routes } from "@/shared/config/routes";
import { getMyCourses } from "@/features/course/api/getMyCourses";
import CourseCard from "@/features/course/components/CourseCard";
import ActionButton from "@/shared/components/ActionButton";
import { canCreateCourse } from "@/shared/lib/auth/coursePermissions";

const MyCoursesPage = async () => {
  const session = await getSession();

  const courses = await getMyCourses(session!.accessToken);
  const canCreate = canCreateCourse(session?.user.role);
  return (
    <div>
      <div className="mb-6 flex items-center justify-between gap-4">
        <h1 className="text-2xl font-bold">My Courses</h1>

        {canCreate && (
          <ActionButton
            label="Create course"
            href={routes.newCourse}
            variant="primary"
          />
        )}
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {courses.map((course) => (
          <CourseCard key={course.id} course={course} />
        ))}
      </div>
    </div>
  );
};

export default MyCoursesPage;

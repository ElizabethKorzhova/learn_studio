import { getSession } from "@/shared/lib/auth/getSession";
import { getCourses } from "@/features/course/api/getCourses";
import CourseCard from "@/features/course/components/CourseCard";
import Title from "@/shared/components/Title";

const CoursesPage = async () => {
  const session = await getSession();
  const courses = await getCourses(session!.accessToken);

  return (
    <section className="mx-auto w-full max-w-7xl space-y-8">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div className="space-y-1">
          <Title title="Courses" />
        </div>
      </div>
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {courses.map((course) => (
          <CourseCard key={course.id} course={course} />
        ))}
      </div>
    </section>
  );
};

export default CoursesPage;

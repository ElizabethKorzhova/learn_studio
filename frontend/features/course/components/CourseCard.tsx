import ActionButton from "@/shared/components/ActionButton";
import { routes } from "@/shared/config/routes";
import type { CourseCardProps } from "../types/course.types";
import { formatDate } from "@/shared/lib/date/formatDate";

const CourseCard = ({ course }: CourseCardProps) => {
  return (
    <div className="ring-primary-light flex h-full flex-col rounded-3xl bg-white p-6 shadow-sm ring-1 transition hover:shadow-md">
      <div className="flex-1">
        <div className="mb-4 flex flex-wrap justify-between">
          <span className="bg-primary-light text-primary-grey/70 inline-flex items-center rounded-full px-3 py-1 text-[10px] font-black tracking-widest uppercase">
            {course.duration} lessons
          </span>

          <span className="bg-primary-light text-primary-grey/70 inline-flex items-center rounded-full px-3 py-1 text-[10px] font-black tracking-widest uppercase">
            {formatDate(course.start_at)}
          </span>
        </div>

        <h3 className="text-primary-dark mb-2 text-xl leading-tight font-bold">
          {course.title}
        </h3>

        <p className="text-primary-grey mb-6 line-clamp-3 text-sm leading-relaxed">
          {course.description}
        </p>
      </div>

      <ActionButton
        label="Open course"
        href={routes.course(String(course.id))}
        variant="outline"
        className="w-full"
      />
    </div>
  );
};

export default CourseCard;

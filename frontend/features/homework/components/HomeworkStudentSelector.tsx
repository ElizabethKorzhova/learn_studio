import Link from "next/link";
import { routes } from "@/shared/config/routes";
import { HomeworkStudentSelectorProps } from "@/features/homework/types/homework.types";

const HomeworkStudentSelector = ({
  homeworkId,
  students,
  selectedStudentId,
}: HomeworkStudentSelectorProps) => (
  <section className="ring-primary-light space-y-4 rounded-4xl bg-white p-6 shadow-sm ring-1">
    <p className="text-primary-grey/50 text-[10px] font-black tracking-widest uppercase">
      Select student
    </p>

    {students.length === 0 ? (
      <p className="text-primary-grey text-sm">No students yet.</p>
    ) : (
      <div className="flex flex-wrap gap-2">
        {students.map((item) => {
          const isActive = selectedStudentId === item.student.id;

          return (
            <Link
              key={item.student.id}
              href={`${routes.homework(homeworkId)}?student_id=${item.student.id}`}
              className={`rounded-2xl px-4 py-2 text-sm font-bold transition ${
                isActive
                  ? "bg-primary-accent shadow-primary-accent/20 text-white shadow-sm"
                  : "bg-primary-light/40 text-primary-dark hover:bg-primary-light"
              }`}
            >
              {item.student.first_name} {item.student.last_name}
            </Link>
          );
        })}
      </div>
    )}
  </section>
);

export default HomeworkStudentSelector;

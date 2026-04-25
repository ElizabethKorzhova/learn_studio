import Link from "next/link";
import GradeSubmissionForm from "@/features/submission/components/GradeSubmissionForm";
import { formatDateTime } from "@/shared/lib/date/formatDate";
import { HomeworkSubmissionsProps } from "@/features/homework/types/homework.types";

const HomeworkSubmissions = ({
  submissions,
  canGrade,
}: HomeworkSubmissionsProps) => {
  if (submissions.length === 0) {
    return (
      <div className="border-primary-light text-primary-grey rounded-4xl border-2 border-dashed p-10 text-center text-sm">
        No submissions found.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {submissions.map((submission) => (
        <article
          key={submission.id}
          className="ring-primary-light rounded-3xl bg-white p-5 shadow-sm ring-1"
        >
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-primary-dark font-bold">
                {submission.user.first_name} {submission.user.last_name}
              </p>

              <p className="text-primary-grey text-xs">
                Submitted: {formatDateTime(submission.submitted_at)} · Score:{" "}
                <span className="text-primary-accent font-bold">
                  {submission.score ?? "Not graded yet"}
                </span>
              </p>
            </div>

            {submission.url && (
              <Link
                href={submission.url}
                target="_blank"
                className="bg-primary-light text-primary-accent hover:bg-primary-accent rounded-xl px-4 py-2 text-[10px] font-black tracking-widest uppercase transition hover:text-white"
              >
                Open solution
              </Link>
            )}
          </div>

          {canGrade && (
            <GradeSubmissionForm
              submissionId={submission.id}
              initialScore={submission.score}
            />
          )}
        </article>
      ))}
    </div>
  );
};

export default HomeworkSubmissions;

"use client";

import { Form, Formik } from "formik";
import { useRouter } from "next/navigation";
import * as Yup from "yup";

import { gradeSubmission } from "@/features/submission/api/gradeSubmission";
import ActionButton from "@/shared/components/ActionButton";
import TextField from "@/shared/components/forms/TextField";

type GradeSubmissionFormProps = {
  submissionId: number;
  initialScore?: number | null;
};

const gradeSchema = Yup.object({
  score: Yup.number()
    .typeError("Score must be a number")
    .min(0, "Score must be at least 0")
    .max(100, "Score must be at most 100")
    .required("Score is required"),
});

const GradeSubmissionForm = ({
  submissionId,
  initialScore,
}: GradeSubmissionFormProps) => {
  const router = useRouter();

  return (
    <Formik
      initialValues={{
        score: initialScore ?? "",
      }}
      validationSchema={gradeSchema}
      onSubmit={async (values, { setSubmitting, setStatus }) => {
        try {
          setStatus(null);

          await gradeSubmission(submissionId, {
            score: Number(values.score),
          });

          router.refresh();
        } catch (error) {
          setStatus(
            error instanceof Error
              ? error.message
              : "Failed to grade submissions",
          );
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ isSubmitting, status }) => (
        <Form className="mt-4 space-y-3">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start">
            <div className="w-full sm:w-32">
              <TextField name="score" label="Score" type="number" />
            </div>

            <div className="pt-5">
              <ActionButton
                label="Grade"
                type="submit"
                variant="outline"
                disabled={isSubmitting}
              />
            </div>
          </div>

          {status && (
            <p className="text-sm font-medium text-red-500">{status}</p>
          )}
        </Form>
      )}
    </Formik>
  );
};

export default GradeSubmissionForm;

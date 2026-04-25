"use client";

import { Form, Formik } from "formik";
import { useRouter } from "next/navigation";
import * as Yup from "yup";

import { createSubmission } from "@/features/submission/api/createSubmission";
import ActionButton from "@/shared/components/ActionButton";
import TextField from "@/shared/components/forms/TextField";

const submissionSchema = Yup.object({
  url: Yup.string().url("Invalid URL").required("URL is required"),
});

export function SubmissionForm({ homeworkId }: { homeworkId: number }) {
  const router = useRouter();

  return (
    <Formik
      initialValues={{ url: "" }}
      validationSchema={submissionSchema}
      onSubmit={async (values, { setSubmitting, setStatus, resetForm }) => {
        try {
          setStatus(null);

          await createSubmission(homeworkId, values);

          resetForm();
          router.refresh();
        } catch (error) {
          setStatus(
            error instanceof Error ? error.message : "Submission failed",
          );
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ isSubmitting, status }) => (
        <Form className="space-y-4">
          <TextField
            name="url"
            type="url"
            label="Solution URL"
            placeholder="https://github.com/..."
          />

          {status && (
            <div className="px-1 text-xs font-bold text-red-500">{status}</div>
          )}

          <ActionButton
            label={isSubmitting ? "Sending..." : "Submit solution"}
            type="submit"
            disabled={isSubmitting}
            className="w-full"
          />
        </Form>
      )}
    </Formik>
  );
}

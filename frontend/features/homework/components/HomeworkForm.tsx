"use client";

import { Form, Formik } from "formik";
import { useRouter } from "next/navigation";
import type {
  Homework,
  HomeworkPayload,
} from "@/features/homework/types/homework.types";
import { homeworkSchema } from "@/features/homework/schemas/homeworkSchema";
import ActionButton from "@/shared/components/ActionButton";
import BackButton from "@/shared/components/BackButton";
import TextareaField from "@/shared/components/forms/TextareaField";
import TextField from "@/shared/components/forms/TextField";
import Title from "@/shared/components/Title";
import { routes } from "@/shared/config/routes";
import type {
  HomeworkFormValues,
  HomeworkFormProps,
} from "@/features/homework/types/homework.types";

const formatDateTimeLocalValue = (value?: string) => {
  if (!value) return "";

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) return "";

  const offsetMs = date.getTimezoneOffset() * 60_000;

  return new Date(date.getTime() - offsetMs).toISOString().slice(0, 16);
};

const getInitialValues = (homework?: Homework): HomeworkFormValues => ({
  title: homework?.title ?? "",
  task: homework?.task ?? "",
  deadline: formatDateTimeLocalValue(homework?.deadline),
  complexity: homework?.complexity ?? 1,
});

const toPayload = (values: HomeworkFormValues): HomeworkPayload => {
  const deadline = new Date(values.deadline);

  return {
    title: values.title,
    task: values.task,
    deadline: deadline.toISOString(),
    deadline_date: deadline.toISOString().slice(0, 10),
    complexity: Number(values.complexity),
  };
};

const HomeworkForm = ({
  mode,
  lessonId,
  homeworkId,
  initialValues,
  title,
  submitLabel,
}: HomeworkFormProps) => {
  const router = useRouter();

  const handleSubmit = async (values: HomeworkFormValues) => {
    if (mode === "create" && !lessonId) {
      throw new Error("Lesson id is required");
    }

    if (mode === "edit" && !homeworkId) {
      throw new Error("Homework id is required");
    }

    const url =
      mode === "create"
        ? routes.api.homeworks(lessonId!)
        : routes.api.homework(homeworkId!);

    const response = await fetch(url, {
      method: mode === "create" ? "POST" : "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(toPayload(values)),
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      throw new Error(
        data?.message || data?.detail || "Failed to save homework",
      );
    }

    return data as Homework;
  };

  return (
    <section className="mx-auto w-full max-w-4xl space-y-4">
      <BackButton />

      <Formik
        initialValues={getInitialValues(initialValues)}
        validationSchema={homeworkSchema}
        onSubmit={async (values, { setSubmitting, setStatus }) => {
          try {
            setStatus(null);

            const savedHomework = await handleSubmit(values);

            router.push(routes.homework(savedHomework.id));
            router.refresh();
          } catch (error) {
            setStatus(
              error instanceof Error
                ? error.message
                : "Failed to save homework",
            );
          } finally {
            setSubmitting(false);
          }
        }}
      >
        {({ isSubmitting, status }) => (
          <Form className="ring-primary-light space-y-8 rounded-[40px] bg-white p-10 shadow-sm ring-1">
            <Title title={title} />

            <div className="space-y-6">
              <TextField
                name="title"
                label="Homework Title"
                placeholder="Enter homework title"
              />

              <TextareaField
                name="task"
                label="Task"
                placeholder="Describe the assignment"
                rows={8}
              />

              <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                <TextField
                  name="deadline"
                  label="Deadline"
                  type="datetime-local"
                />

                <TextField name="complexity" label="Complexity" type="number" />
              </div>
            </div>

            {status && (
              <div className="rounded-2xl border border-red-100 bg-red-50 p-4 text-center text-sm font-bold text-red-600">
                {status}
              </div>
            )}

            <div className="flex items-center justify-end gap-4 pt-8">
              <ActionButton
                label="Cancel"
                variant="outline"
                onClick={() => router.back()}
              />

              <ActionButton
                label={isSubmitting ? "Saving..." : submitLabel}
                type="submit"
                variant="primary"
                disabled={isSubmitting}
              />
            </div>
          </Form>
        )}
      </Formik>
    </section>
  );
};

export default HomeworkForm;

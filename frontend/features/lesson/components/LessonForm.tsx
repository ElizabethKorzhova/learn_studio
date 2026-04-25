"use client";

import { Form, Formik } from "formik";
import { useRouter } from "next/navigation";
import type {
  Lesson,
  LessonPayload,
} from "@/features/lesson/types/lesson.types";
import ActionButton from "@/shared/components/ActionButton";
import BackButton from "@/shared/components/BackButton";
import TextareaField from "@/shared/components/forms/TextareaField";
import TextField from "@/shared/components/forms/TextField";
import Title from "@/shared/components/Title";
import { routes } from "@/shared/config/routes";
import type {
  LessonFormValues,
  LessonFormProps,
} from "@/features/lesson/types/lesson.types";
import { lessonSchema } from "@/features/lesson/schemas/lesson.types";

const getInitialValues = (lesson?: Lesson): LessonFormValues => ({
  title: lesson?.title ?? "",
  content: lesson?.content ?? "",
  order_index: lesson?.order_index ?? 0,
  images: lesson?.images ?? "",
});

const toPayload = (values: LessonFormValues): LessonPayload => ({
  title: values.title,
  content: values.content,
  order_index: Number(values.order_index),
  images: values.images || null,
});

const LessonForm = ({
  mode,
  courseId,
  lessonId,
  initialValues,
  submitLabel,
  title,
}: LessonFormProps) => {
  const router = useRouter();

  const handleSubmit = async (values: LessonFormValues) => {
    if (mode === "edit" && !lessonId) {
      throw new Error("Lesson id is required for editing");
    }

    const url =
      mode === "create"
        ? routes.api.lessons(String(courseId))
        : `${routes.api.lesson(String(lessonId!))}?course_id=${courseId}`;

    const response = await fetch(url, {
      method: mode === "create" ? "POST" : "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(toPayload(values)),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);

      throw new Error(
        errorData?.message || errorData?.detail || "Failed to save lesson",
      );
    }

    return (await response.json()) as Promise<Lesson>;
  };

  return (
    <section className="mx-auto w-full max-w-4xl space-y-4">
      <BackButton />

      <Formik
        initialValues={getInitialValues(initialValues)}
        validationSchema={lessonSchema}
        onSubmit={async (values, { setSubmitting, setStatus }) => {
          try {
            setStatus(null);

            const savedLesson = await handleSubmit(values);

            const redirectUrl =
              mode === "create"
                ? routes.course(String(courseId))
                : `${routes.lesson(String(savedLesson.id))}?course_id=${courseId}`;

            router.push(redirectUrl);
          } catch (error) {
            setStatus(
              error instanceof Error ? error.message : "Failed to save lesson",
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
                label="Lesson Title"
                placeholder="Enter lesson title"
              />

              <TextField
                name="order_index"
                label="Lesson Order"
                type="number"
              />

              <TextareaField
                name="content"
                label="Content"
                placeholder="Write lesson content"
                rows={8}
              />
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

export default LessonForm;

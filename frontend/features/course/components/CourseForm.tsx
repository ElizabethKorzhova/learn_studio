"use client";

import { Form, Formik } from "formik";
import { useRouter } from "next/navigation";

import type {
  Course,
  CoursePayload,
} from "@/features/course/types/course.types";
import { courseSchema } from "@/features/course/schemas/courseSchema";
import ActionButton from "@/shared/components/ActionButton";
import BackButton from "@/shared/components/BackButton";
import TextareaField from "@/shared/components/forms/TextareaField";
import TextField from "@/shared/components/forms/TextField";
import Title from "@/shared/components/Title";
import { routes } from "@/shared/config/routes";
import {
  CourseFormValues,
  CourseFormProps,
} from "@/features/course/types/course.types";

const getInitialValues = (
  initialValues?: Course | CoursePayload,
): CourseFormValues => ({
  title: initialValues?.title ?? "",
  description: initialValues?.description ?? "",
  start_at: initialValues?.start_at
    ? new Date(initialValues.start_at).toISOString().slice(0, 16)
    : "",
  duration: initialValues?.duration ?? 0,
  price: initialValues?.price ?? "",
});

const createCoursePayload = (values: CourseFormValues): CoursePayload => ({
  title: values.title,
  description: values.description,
  start_at: new Date(values.start_at).toISOString(),
  duration: Number(values.duration),
  price: values.price ? String(values.price) : null,
});

const CourseForm = ({
  mode,
  courseId,
  initialValues,
  submitLabel,
  title,
}: CourseFormProps) => {
  const router = useRouter();

  const handleSubmit = async (values: CourseFormValues) => {
    if (mode === "edit" && !courseId) {
      throw new Error("Course id is required for editing");
    }

    const url =
      mode === "create"
        ? routes.api.courses
        : routes.api.course(String(courseId));

    const response = await fetch(url, {
      method: mode === "create" ? "POST" : "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(createCoursePayload(values)),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);

      throw new Error(
        errorData?.message || errorData?.detail || "Failed to save course",
      );
    }

    return (await response.json()) as Promise<Course>;
  };

  return (
    <section className="mx-auto w-full max-w-4xl space-y-4">
      <BackButton />
      <Formik
        initialValues={getInitialValues(initialValues)}
        validationSchema={courseSchema}
        onSubmit={async (values, { setSubmitting, setStatus }) => {
          try {
            setStatus(null);

            const savedCourse = await handleSubmit(values);

            router.push(routes.course(String(savedCourse.id)));
            router.refresh();
          } catch (error) {
            setStatus(
              error instanceof Error ? error.message : "Failed to save course",
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
                label="Course Title"
                placeholder="Enter title"
              />

              <TextareaField
                name="description"
                label="Description"
                placeholder="Tell more about the course"
              />

              <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                <TextField
                  name="start_at"
                  label="Start Date"
                  type="datetime-local"
                />

                <TextField
                  name="duration"
                  label="Duration (lessons count)"
                  type="number"
                />
              </div>

              <TextField
                name="price"
                label="Price"
                type="number"
                placeholder="Free course"
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
                variant="primary"
                type="submit"
                disabled={isSubmitting}
                className="min-w-35"
              />
            </div>
          </Form>
        )}
      </Formik>
    </section>
  );
};

export default CourseForm;

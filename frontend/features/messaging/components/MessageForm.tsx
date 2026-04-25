"use client";

import { ErrorMessage, Field, Form, Formik } from "formik";
import * as Yup from "yup";

import { sendHomeworkMessage } from "@/features/messaging/api/sendHomeworkMessage";
import ActionButton from "@/shared/components/ActionButton";
import { MessageFormProps } from "@/features/messaging/types/message.types";

const messageSchema = Yup.object({
  message_text: Yup.string().trim().required("Message is required"),
});

export function MessageForm({
  homeworkId,
  studentId,
  onSuccess,
}: MessageFormProps) {
  return (
    <Formik
      initialValues={{ message_text: "" }}
      validationSchema={messageSchema}
      onSubmit={async (values, { setSubmitting, setStatus, resetForm }) => {
        try {
          setStatus(null);

          const message = await sendHomeworkMessage(
            homeworkId,
            values,
            studentId,
          );

          resetForm();
          onSuccess?.(message);
        } catch (error) {
          setStatus(
            error instanceof Error ? error.message : "Failed to send message",
          );
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ isSubmitting, status }) => (
        <Form className="space-y-3">
          <div>
            <Field
              as="textarea"
              name="message_text"
              placeholder="Write a message..."
              rows={4}
              className="border-primary-light bg-primary-light/10 text-primary-dark focus:ring-primary-accent/10 min-h-28 w-full resize-y rounded-2xl border p-4 text-sm transition outline-none focus:bg-white focus:ring-2"
            />

            <ErrorMessage
              name="message_text"
              component="div"
              className="mt-1 px-1 text-xs font-medium text-red-500"
            />
          </div>

          {status && (
            <p className="text-sm font-medium text-red-500">{status}</p>
          )}

          <div className="flex justify-end">
            <ActionButton
              label={isSubmitting ? "Sending..." : "Send message"}
              type="submit"
              disabled={isSubmitting}
            />
          </div>
        </Form>
      )}
    </Formik>
  );
}

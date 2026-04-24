"use client";

import { Form, Formik } from "formik";
import { CurrentUser } from "@/features/auth/types/auth.types";
import { profileSchema } from "@/features/profile/schemas/profileSchema";
import TextField from "@/shared/components/forms/TextField";
import ActionButton from "@/shared/components/ActionButton";
import { ProfileEditFormProps } from "@/features/profile/types/profile.types";

const ProfileEditForm = ({
  profile,
  onCancel,
  onSuccess,
}: ProfileEditFormProps) => {
  return (
    <Formik
      initialValues={{
        username: profile.username,
        email: profile.email,
        first_name: profile.first_name,
        last_name: profile.last_name,
      }}
      validationSchema={profileSchema}
      onSubmit={async (values, { setSubmitting, setStatus }) => {
        setStatus(undefined);

        try {
          const response = await fetch("api/profile", {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(values),
          });

          if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            throw new Error(
              errorData?.message ||
                errorData?.detail ||
                "Failed to update profile",
            );
          }

          const updatedProfile = (await response.json()) as CurrentUser;
          onSuccess(updatedProfile);
        } catch (error) {
          setStatus(
            error instanceof Error
              ? error.message
              : "Failed to update profile.",
          );
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ isSubmitting, status }) => (
        <Form className="ring-primary-light space-y-6 rounded-3xl bg-white p-6 shadow-sm ring-1">
          <div className="flex items-center justify-between">
            <h3 className="text-primary-dark text-lg font-bold">
              Edit Information
            </h3>

            <ActionButton
              label="Cancel"
              variant="xs-ghost"
              onClick={onCancel}
            />
          </div>

          <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
            <TextField
              name="first_name"
              label="First name"
              placeholder="Enter first name"
            />

            <TextField
              name="last_name"
              label="Last name"
              placeholder="Enter last name"
            />

            <TextField
              name="username"
              label="Username"
              placeholder="Enter username"
            />

            <TextField
              name="email"
              label="Email"
              type="email"
              placeholder="Enter email"
            />
          </div>

          {status && (
            <div className="rounded-2xl bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
              {status}
            </div>
          )}

          <div className="flex justify-end gap-3">
            <ActionButton
              label="Discard"
              variant="outline"
              onClick={onCancel}
              disabled={isSubmitting}
            />

            <ActionButton
              label={isSubmitting ? "Saving..." : "Save changes"}
              type="submit"
              disabled={isSubmitting}
            />
          </div>
        </Form>
      )}
    </Formik>
  );
};

export default ProfileEditForm;

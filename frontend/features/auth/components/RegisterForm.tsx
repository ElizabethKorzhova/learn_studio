"use client";

import { useRouter } from "next/navigation";
import { Formik, Form } from "formik";
import { register } from "../api/register";
import { registerSchema } from "../schemas/registerSchema";
import TextField from "@/shared/components/forms/TextField";
import SelectField from "@/shared/components/forms/SelectField";
import AuthQuestion from "@/features/auth/components/AuthQuestion";
import { routes } from "@/shared/config/routes";
import ActionButton from "@/shared/components/ActionButton";

const RegisterForm = () => {
  const router = useRouter();

  return (
    <Formik
      initialValues={{
        email: "",
        username: "",
        password: "",
        first_name: "",
        last_name: "",
        role: "student",
      }}
      validationSchema={registerSchema}
      onSubmit={async (values, { setStatus, setSubmitting }) => {
        try {
          setStatus(null);
          await register(values);
          router.push(routes.courses);
          router.refresh();
        } catch (error) {
          const message =
            error instanceof Error ? error.message : "Registration failed";
          setStatus(message);
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ status }) => (
        <Form className="flex w-full max-w-md flex-col gap-4 lg:gap-6">
          <div className="flex w-full gap-4">
            <div className="min-w-0 flex-1">
              <TextField
                name="first_name"
                label="First Name"
                placeholder="First name"
              />
            </div>
            <div className="min-w-0 flex-1">
              <TextField
                name="last_name"
                label="Last Name"
                placeholder="Last name"
              />
            </div>
          </div>

          <TextField
            name="username"
            label="Username"
            placeholder="Enter username"
          />
          <TextField
            name="email"
            type="email"
            label="Email"
            placeholder="Enter your email"
          />

          <SelectField name="role" label="I am a/an">
            <option value="student">Student</option>
            <option value="instructor">Instructor</option>
          </SelectField>

          <TextField
            name="password"
            type="password"
            label="Password"
            placeholder="••••••••"
          />
          <AuthQuestion
            question="Have you already had the account"
            route={routes.login}
            linkTitle="Login"
          />

          {status && (
            <div className="text-primary-red text-center text-sm font-medium">
              {status}
            </div>
          )}
          <ActionButton
            label="Register"
            variant="dark"
            type="submit"
            className="w-full"
          />
        </Form>
      )}
    </Formik>
  );
};

export default RegisterForm;

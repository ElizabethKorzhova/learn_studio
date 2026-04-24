"use client";

import { useRouter } from "next/navigation";
import { Formik, Form } from "formik";
import { login } from "../api/login";
import { loginSchema } from "../schemas/loginSchema";
import TextField from "@/shared/components/forms/TextField";
import AuthQuestion from "@/features/auth/components/AuthQuestion";
import { routes } from "@/shared/config/routes";
import ActionButton from "@/shared/components/ActionButton";

const LoginForm = () => {
  const router = useRouter();

  return (
    <Formik
      initialValues={{
        email: "",
        password: "",
      }}
      validationSchema={loginSchema}
      onSubmit={async (values, { setSubmitting, setStatus }) => {
        try {
          setStatus(null);
          await login(values);
          router.push(routes.dashboard);
          router.refresh();
        } catch (error) {
          const message =
            error instanceof Error ? error.message : "Login failed";
          setStatus(message);
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ status }) => (
        <Form className="flex flex-col gap-4 lg:gap-6">
          <TextField
            name="email"
            type="email"
            label="Email"
            placeholder="Enter your email"
          />

          <TextField
            name="password"
            type="password"
            label="Password"
            placeholder="••••••••"
          />

          {status && (
            <div className="text-primary-red text-center text-sm">{status}</div>
          )}
          <AuthQuestion
            question="Do not have an account"
            route={routes.register}
            linkTitle="Register"
          />
          <ActionButton
            label="Login"
            variant="dark"
            type="submit"
            className="w-full"
          />
        </Form>
      )}
    </Formik>
  );
};

export default LoginForm;

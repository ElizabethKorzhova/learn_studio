import type { AuthFormWrapperProps } from "@/features/auth/types/auth.types";
import PublicHeader from "@/shared/components/PublicHeader";
import { getSession } from "@/shared/lib/auth/getSession";
import { redirect } from "next/navigation";
import { routes } from "@/shared/config/routes";
import Title from "@/shared/components/Title";

const AuthPageWrapper = async ({ title, children }: AuthFormWrapperProps) => {
  const session = await getSession();

  if (session) {
    redirect(routes.dashboard);
  }

  return (
    <>
      <PublicHeader showNavigation={false} />
      <section className="bg-secondary-light flex min-h-screen items-center justify-center p-6 px-6 pb-6 md:px-18 md:pb-10 lg:pb-16 lg:pb-32">
        <div className="shadow-primary-soft border-primary-light w-full max-w-md rounded-2xl border bg-white p-6">
          <Title title={title} />
          {children}
        </div>
      </section>
    </>
  );
};

export default AuthPageWrapper;

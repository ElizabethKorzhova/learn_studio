import ActionButton from "@/shared/components/ActionButton";
import { routes } from "@/shared/config/routes";

const NotFound = () => (
  <main className="flex min-h-[70vh] items-center justify-center px-4">
    <section className="ring-primary-light w-full max-w-xl rounded-4xl bg-white p-10 text-center shadow-sm ring-1">
      <div className="text-primary-accent mx-auto mb-6 flex h-16 w-16 items-center justify-center text-6xl font-black">
        404
      </div>

      <h1 className="text-primary-dark text-3xl font-bold tracking-tight">
        Page not found
      </h1>

      <p className="text-primary-grey mx-auto mt-3 max-w-md text-sm leading-relaxed">
        The page you are looking for does not exist, was moved, or you do not
        have access to it.
      </p>

      <div className="mt-8 flex justify-center">
        <ActionButton
          label="Back to courses"
          href={routes.courses}
          variant="primary"
        />
      </div>
    </section>
  </main>
);

export default NotFound;

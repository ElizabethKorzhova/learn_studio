import { routes } from "@/shared/config/routes";
import Logo from "@/shared/components/Logo";
import type { PublicHeaderProps } from "@/shared/types/ui.types";
import ActionButton from "@/shared/components/ActionButton";

const PublicHeader = ({ showNavigation = true }: PublicHeaderProps) => {
  return (
    <header
      className={`flex items-center justify-between px-6 pt-6 md:px-18 md:pt-10 lg:px-32 lg:pt-16 ${showNavigation ? "bg-transparent" : "bg-secondary-light"}`}
    >
      <Logo />
      {showNavigation && (
        <nav>
          <ul className="flex items-center gap-4 lg:gap-8">
            <li>
              <ActionButton href={routes.login} label="Login" variant="dark" />
            </li>
            <li>
              <ActionButton
                href={routes.register}
                label="Register"
                variant="dark"
              />
            </li>
          </ul>
        </nav>
      )}
    </header>
  );
};

export default PublicHeader;

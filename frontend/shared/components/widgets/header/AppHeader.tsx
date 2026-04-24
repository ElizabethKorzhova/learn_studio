import type { AppHeaderProps } from "@/shared/types/widget.types";
import LogoutButton from "@/shared/components/LogoutButton";

const AppHeader = ({ user }: AppHeaderProps) => {
  return (
    <header className="sticky top-0 z-50 flex items-center justify-end gap-4 bg-white px-6 py-4">
      <span className="text-sm">
        {user.first_name} {user.last_name}
      </span>
      <LogoutButton />
    </header>
  );
};

export default AppHeader;

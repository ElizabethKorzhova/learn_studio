import type { CurrentUser } from "@/features/auth/types/auth.types";

export interface AppHeaderProps {
  user: CurrentUser;
}

export type SidebarNavItemProps = {
  href: string;
  label: string;
  exact?: boolean;
  className?: string;
};

export type SidebarProps = {
  user: CurrentUser;
};

export type BurgerButtonProps = {
  onClick: () => void;
};

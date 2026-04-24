"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { SidebarNavItemProps } from "@/shared/types/widget.types";

const SidebarNavItem = ({
  href,
  label,
  exact = false,
  className = "",
}: SidebarNavItemProps) => {
  const pathname = usePathname();

  const isActive = exact ? pathname === href : pathname.startsWith(href);

  return (
    <Link
      href={href}
      className={[
        "block rounded-xl px-4 py-3 text-sm font-medium transition-colors",
        isActive
          ? "bg-primary-light text-primary-accent"
          : "text-primary-grey hover:bg-primary-light hover:text-primary-accent",
        className,
      ].join(" ")}
    >
      {label}
    </Link>
  );
};

export default SidebarNavItem;

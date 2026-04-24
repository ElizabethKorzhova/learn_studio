"use client";

import Link from "next/link";
import { ActionButtonProps } from "@/shared/types/ui.types";

const ActionButton = ({
  label,
  href,
  onClick,
  variant = "primary",
  className = "",
  type = "button",
  confirmMessage,
  disabled = false,
}: ActionButtonProps) => {
  const handleInternalClick = (
    event: React.MouseEvent<HTMLButtonElement | HTMLAnchorElement>,
  ) => {
    if (confirmMessage && !window.confirm(confirmMessage)) {
      event.preventDefault();
      return;
    }
    onClick?.(event);
  };

  const baseStyles =
    "flex items-center justify-center rounded-2xl px-5 py-3 text-sm font-bold transition-all disabled:opacity-50 cursor-pointer disabled:cursor-not-allowed";

  const variants = {
    primary:
      "bg-primary-accent text-white hover:opacity-90 shadow-sm shadow-primary-accent/20",
    outline:
      "bg-white text-primary-accent ring-1 ring-primary-light hover:bg-primary-light",
    dark: "bg-primary-dark text-white hover:bg-opacity-90 hover:bg-primary-accent",
    "danger-ghost":
      "text-red-500 hover:bg-red-50 border border-transparent hover:border-red-100",
    "xs-ghost":
      "px-3 py-2 text-xs font-black uppercase tracking-widest text-primary-grey hover:bg-primary-light hover:text-primary-accent",
    "xs-danger":
      "px-3 py-2 text-xs font-black uppercase tracking-widest text-red-400 hover:bg-red-50 hover:text-red-600",
  };

  const finalClass = `${baseStyles} ${variants[variant]} ${className}`;

  if (href) {
    return (
      <Link href={href} className={finalClass} onClick={handleInternalClick}>
        {label}
      </Link>
    );
  }

  return (
    <button
      type={type}
      className={finalClass}
      onClick={handleInternalClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
};

export default ActionButton;

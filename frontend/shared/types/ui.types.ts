import React from "react";

export interface ActionButtonProps {
  label: string;
  href?: string;
  onClick?: (
    event: React.MouseEvent<HTMLButtonElement | HTMLAnchorElement>,
  ) => void;
  variant?:
    | "primary"
    | "outline"
    | "dark"
    | "danger-ghost"
    | "xs-ghost"
    | "xs-danger";
  className?: string;
  type?: "button" | "submit";
  confirmMessage?: string;
  disabled?: boolean;
}

export interface PublicHeaderProps {
  showNavigation?: boolean;
}

export interface TitleProps {
  title: string;
}

"use client";

import ActionButton from "@/shared/components/ActionButton";
import { logout } from "@/features/auth/api/logout";
import { routes } from "@/shared/config/routes";

const LogoutButton = () => {
  const handleLogout = async () => {
    try {
      const result = await logout();

      if (result.ok) {
        window.location.href = routes.login;
      }
    } catch (error) {
      console.error("Logout failed", error);
    }
  };

  return <ActionButton label="Logout" variant="dark" onClick={handleLogout} />;
};

export default LogoutButton;

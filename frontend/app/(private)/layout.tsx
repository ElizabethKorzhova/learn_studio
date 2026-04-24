import React from "react";
import { redirect } from "next/navigation";
import { getSession } from "@/shared/lib/auth/getSession";
import Sidebar from "@/shared/components/widgets/sidebar/Sidebar";
import AppHeader from "@/shared/components/widgets/header/AppHeader";
import SidebarWrapper from "@/shared/components/widgets/sidebar/SidebarWrapper";
import { routes } from "@/shared/config/routes";

const PrivateLayout = async ({ children }: { children: React.ReactNode }) => {
  const session = await getSession();

  if (!session) {
    redirect(routes.login);
  }

  return (
    <div className="bg-primary-light/20 flex min-h-screen">
      <SidebarWrapper>
        <Sidebar user={session.user} />
      </SidebarWrapper>

      <div className="flex min-w-0 flex-1 flex-col">
        <AppHeader user={session.user} />

        <main className="p-4 md:p-8 lg:p-10">{children}</main>
      </div>
    </div>
  );
};

export default PrivateLayout;

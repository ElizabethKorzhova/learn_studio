import { routes } from "@/shared/config/routes";
import { SidebarProps } from "@/shared/types/widget.types";
import SidebarNavItem from "@/shared/components/widgets/sidebar/SidebarNavItem";
import Logo from "@/shared/components/Logo";

const Sidebar = ({ user }: SidebarProps) => {
  const navLinks = [
    { name: "My profile", href: routes.profile },
    { name: "Courses", href: routes.courses },
    { name: "My Courses", href: routes.myCourses },
  ];

  return (
    <div className="flex h-full flex-col">
      <div className="hidden p-6 lg:block">
        <Logo />
      </div>

      <nav className="flex-1 space-y-6 overflow-y-auto px-4 pb-4">
        <div className="space-y-1">
          {navLinks.map((link) => (
            <SidebarNavItem
              key={link.href}
              href={link.href}
              label={link.name}
            />
          ))}
        </div>
      </nav>

      <div className="p-6">
        <div className="text-primary-grey/50 flex items-center gap-2 text-[10px] font-black tracking-widest uppercase">
          {user.role}
        </div>
      </div>
    </div>
  );
};

export default Sidebar;

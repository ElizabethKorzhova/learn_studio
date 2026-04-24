"use client";

import React from "react";
import { useEffect, useState } from "react";
import BurgerButton from "@/shared/components/widgets/header/BurgerButton";

const SidebarWrapper = ({ children }: { children: React.ReactNode }) => {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    document.body.style.overflow = isOpen ? "hidden" : "unset";

    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  const closeSidebar = () => {
    setIsOpen(false);
  };

  return (
    <>
      <div className="fixed top-3 left-4 z-60 lg:hidden">
        <BurgerButton onClick={() => setIsOpen(true)} />
      </div>

      {isOpen && (
        <div
          className="bg-primary-dark/40 fixed inset-0 z-70 backdrop-blur-sm lg:hidden"
          onClick={closeSidebar}
        />
      )}

      <aside
        className={[
          "lg:border-primary-light fixed inset-y-0 left-0 z-80 w-[280px] bg-white transition-transform duration-300 ease-in-out sm:w-72 lg:sticky lg:top-0 lg:h-screen lg:translate-x-0 lg:border-r",
          isOpen ? "translate-x-0" : "-translate-x-full",
        ].join(" ")}
      >
        <div className="border-primary-light flex h-16 items-center justify-between border-b px-6 lg:hidden">
          <span className="text-primary-dark text-xl font-bold tracking-tighter">
            Learn Studio
          </span>

          <button
            type="button"
            aria-label="Close sidebar"
            onClick={closeSidebar}
            className="text-primary-grey -mr-2 p-2"
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
        {children}
      </aside>
    </>
  );
};

export default SidebarWrapper;

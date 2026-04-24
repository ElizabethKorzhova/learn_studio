"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import ActionButton from "@/shared/components/ActionButton";
import { routes } from "@/shared/config/routes";
import type { UserProfileCardProps } from "@/features/profile/types/profile.types";

const UserProfileCard = ({ profile, onEdit }: UserProfileCardProps) => {
  const router = useRouter();
  const [isDeleting, setIsDeleting] = useState(false);

  const fullName = `${profile.first_name} ${profile.last_name}`.trim();

  const handleDelete = async () => {
    setIsDeleting(true);

    try {
      const response = await fetch("api/profile", {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Failed to delete account");
      }

      router.push(routes.home);
      router.refresh();
    } catch {
      alert("Failed to delete account. Please try again.");
      setIsDeleting(false);
    }
  };

  return (
    <section className="ring-primary-light flex h-fit flex-col rounded-3xl bg-white p-6 shadow-sm ring-1">
      <div className="flex flex-col items-center text-center">
        <div className="bg-primary-light text-primary-accent flex h-24 w-24 items-center justify-center rounded-full text-2xl font-bold">
          {profile.first_name?.[0]}
          {profile.last_name?.[0]}
        </div>

        <h2 className="text-primary-dark mt-4 text-xl font-bold">
          {fullName || "User profile"}
        </h2>

        <p className="text-primary-grey mt-1 text-sm">{profile.email}</p>

        <div className="bg-primary-light text-primary-grey/70 mt-4 inline-flex items-center gap-2 rounded-full px-3 py-1 text-[11px] font-black tracking-widest uppercase">
          {profile.role}
        </div>

        <ActionButton
          label="Edit Profile"
          variant="outline"
          className="mt-6 w-full"
          onClick={onEdit}
        />
      </div>

      <div className="border-primary-light mt-6 space-y-4 border-t pt-6">
        <div>
          <p className="text-primary-grey/50 text-xs font-black tracking-widest uppercase">
            Username
          </p>
          <p className="text-primary-dark mt-1 text-sm font-medium">
            @{profile.username}
          </p>
        </div>

        {profile.social_links.length > 0 && (
          <div>
            <p className="text-primary-grey/50 mb-2 text-xs font-black tracking-widest uppercase">
              Social Links
            </p>

            <div className="flex flex-wrap gap-2">
              {profile.social_links.map((link) => (
                <a
                  key={`${link.platform_name}-${link.url}`}
                  href={link.url}
                  target="_blank"
                  rel="noreferrer"
                  className="bg-primary-light/50 text-primary-accent hover:bg-primary-light rounded-xl px-3 py-1.5 text-xs font-semibold transition"
                >
                  {link.platform_name}
                </a>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="mt-8 border-t border-red-50 pt-6">
        <ActionButton
          label={isDeleting ? "Deleting..." : "Delete Account"}
          variant="xs-danger"
          className="w-full justify-center"
          disabled={isDeleting}
          onClick={handleDelete}
        />
      </div>
    </section>
  );
};

export default UserProfileCard;

"use client";

import { useState } from "react";
import type { CurrentUser } from "@/features/auth/types/auth.types";
import UserProfileCard from "@/features/profile/components/UserProfileCard";
import ProfileEditForm from "@/features/profile/components/ProfileEditForm";
import Title from "@/shared/components/Title";

const ProfilePageView = ({
  profile: initialProfile,
}: {
  profile: CurrentUser;
}) => {
  const [profile, setProfile] = useState(initialProfile);
  const [isEditing, setIsEditing] = useState(false);

  return (
    <section className="mx-auto w-full max-w-7xl space-y-6">
      <div>
        <Title title="My profile" />
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-[320px_minmax(0,1fr)]">
        <UserProfileCard profile={profile} onEdit={() => setIsEditing(true)} />

        <div className="min-h-[400px]">
          {isEditing ? (
            <ProfileEditForm
              profile={profile}
              onCancel={() => setIsEditing(false)}
              onSuccess={(updatedProfile) => {
                setProfile(updatedProfile);
                setIsEditing(false);
              }}
            />
          ) : (
            <div className="border-primary-light flex h-full items-center justify-center rounded-3xl border-2 border-dashed bg-white/50 p-12 text-center">
              <div className="max-w-xs">
                <h3 className="text-primary-dark text-lg font-bold">
                  Profile Details
                </h3>
                <p className="text-primary-grey mt-2 text-sm">
                  Click the edit button on your profile card to update your
                  information.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default ProfilePageView;

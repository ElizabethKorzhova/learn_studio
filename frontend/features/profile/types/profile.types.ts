import { CurrentUser, SocialLink } from "@/features/auth/types/auth.types";

export type UpdateMyProfilePayload = {
  username?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  social_links?: SocialLink[];
};

export type ProfileEditFormProps = {
  profile: CurrentUser;
  onCancel: () => void;
  onSuccess: (updatedProfile: CurrentUser) => void;
};

export type UserProfileCardProps = {
  profile: CurrentUser;
  onEdit: () => void;
};

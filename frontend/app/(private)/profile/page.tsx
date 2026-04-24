import { redirect } from "next/navigation";
import { getSession } from "@/shared/lib/auth/getSession";
import { routes } from "@/shared/config/routes";
import { getMyProfile } from "@/features/profile/api/getMyProfile";
import ProfilePageView from "@/features/profile/components/ProfilePageView";

const ProfilePage = async () => {
  const session = await getSession();

  if (!session) {
    redirect(routes.login);
  }

  const profile = await getMyProfile(session.accessToken);

  return <ProfilePageView profile={profile} />;
};

export default ProfilePage;

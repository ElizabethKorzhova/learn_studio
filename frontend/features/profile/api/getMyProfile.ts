import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";
import { CurrentUser } from "@/features/auth/types/auth.types";

export async function getMyProfile(accessToken: string): Promise<CurrentUser> {
  return (await baseApi<CurrentUser>(routes.api.profile, {
    accessToken,
  })) as CurrentUser;
}
